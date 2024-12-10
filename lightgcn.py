import os.path as osp

import torch
from tqdm import tqdm

from torch_geometric.datasets import AmazonBook
from torch_geometric.nn import LightGCN
from torch_geometric.utils import degree

import pandas as pd
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# define data class
class Data:
    def __init__(self, train_adj, edge_label_index):
        self.train_adj = train_adj
        self.edge_index = torch.from_numpy(np.concatenate([train_adj, train_adj[[1, 0], :]], axis=1)).to(device)
        self.edge_label_index = torch.from_numpy(edge_label_index).to(device)

path = osp.join(osp.dirname(osp.realpath(__file__)), "data", "Spotify")

df_clean = pd.read_parquet(path + "/packet-0-99-clean.parquet")
num_playlists = df_clean.shape[0]

df_lookup = pd.read_parquet(path + "/lookuptable-0-99.parquet")
num_tracks = df_lookup.shape[0]

train_adj = np.load(path + "/train_adj-0-99.npy")
train_adj[1, :] += num_playlists
test_adj = np.load(path + "/test_adj-0-99.npy")
test_adj[1, :] += num_playlists

data = Data(train_adj, test_adj)

train_edge_label_index = torch.from_numpy(train_adj).to(device)

batch_size = 16384
test_batch_size = 1024
train_loader = torch.utils.data.DataLoader(
    range(train_edge_label_index.size(1)),
    shuffle=True,
    batch_size=batch_size,
)

##########################################

model = LightGCN(
    num_nodes=num_playlists + num_tracks,
    embedding_dim=32,
    num_layers=2,
).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


def train():
    total_loss = total_examples = 0

    for index in tqdm(train_loader):
        # Sample positive and negative labels.
        pos_edge_label_index = train_edge_label_index[:, index]
        neg_edge_label_index = torch.stack(
            [
                pos_edge_label_index[0], # user
                torch.randint(
                    num_playlists, num_playlists + num_tracks, (index.numel(),), device=device
                ), # random book edge
            ],
            dim=0,
        )
        edge_label_index = torch.cat(
            [
                pos_edge_label_index,
                neg_edge_label_index,
            ],
            dim=1,
        )

        optimizer.zero_grad()
        pos_rank, neg_rank = model(data.edge_index, edge_label_index).chunk(2)

        loss = model.recommendation_loss(
            pos_rank,
            neg_rank,
            node_id=edge_label_index.unique(),
        )
        loss.backward()
        optimizer.step()

        total_loss += float(loss) * pos_rank.numel()
        total_examples += pos_rank.numel()

    return total_loss / total_examples


@torch.no_grad()
def test(k: int):
    emb = model.get_embedding(data.edge_index)
    user_emb, book_emb = emb[:num_playlists], emb[num_playlists:]

    precision = recall = total_examples = 0
    for start in tqdm(range(0, num_playlists, test_batch_size)):

        end = min(start + test_batch_size, num_playlists)
        logits = user_emb[start:end] @ book_emb.t()

        # Exclude training edges:
        mask = (train_edge_label_index[0] >= start) & (train_edge_label_index[0] < end)
        logits[
            train_edge_label_index[0, mask] - start,
            train_edge_label_index[1, mask] - num_playlists,
        ] = float("-inf")

        # Computing precision and recall:
        ground_truth = torch.zeros_like(logits, dtype=torch.bool)
        mask = (data.edge_label_index[0] >= start) & (data.edge_label_index[0] < end)

        ground_truth[
            data.edge_label_index[0, mask] - start,
            data.edge_label_index[1, mask] - num_playlists,
        ] = True
        node_count = degree(
            data.edge_label_index[0, mask] - start, num_nodes=logits.size(0)
        )

        topk_index = logits.topk(k, dim=-1).indices
        isin_mat = ground_truth.gather(1, topk_index)

        precision += float((isin_mat.sum(dim=-1) / k).sum())
        recall += float((isin_mat.sum(dim=-1) / node_count.clamp(1e-6)).sum())
        total_examples += int((node_count > 0).sum())

    return precision / total_examples, recall / total_examples


for epoch in range(1, 10):
    loss = train()
    precision, recall = test(k=20)
    print(
        f"Epoch: {epoch:03d}, Loss: {loss:.4f}, Precision@20: "
        f"{precision:.4f}, Recall@20: {recall:.4f}"
    )


#   # Recommendation
#   src_index = 0
#   dst_index = torch.arange(num_playlists, num_playlists + num_tracks, device=device)
#   recommendation = model.recommend(data.edge_index, src_index=src_index, dst_index=dst_index, k=1)
#   
#   df_lookup = pd.read_parquet(path + "/lookuptable-0-9.parquet")
#   
#   track_uri = df_lookup["track"][recommendation[0].item() - num_playlists]
#   print("https://open.spotify.com/track/" + track_uri.split(":")[-1])
