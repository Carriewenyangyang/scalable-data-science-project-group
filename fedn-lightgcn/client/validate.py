import os
import sys
import torch
from model import load_parameters
from data import load_data
from fedn.utils.helpers.helpers import save_metrics
from torch_geometric.utils import degree
from tqdm import tqdm

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(dir_path))


def validate(in_model_path, out_json_path, data_path=None):
    """Validate model.

    :param in_model_path: The path to the input model.
    :type in_model_path: str
    :param out_json_path: The path to save the output JSON to.
    :type out_json_path: str
    :param data_path: The path to the data file.
    :type data_path: str
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    ## Load data
    data = load_data(data_path)
    #num_playlists = 100000
    num_playlists = 1000000
    #num_tracks = 206122
    num_tracks = 857768
    
    train_adj = data.train_adj
    train_edge_label_index = torch.from_numpy(train_adj).to(device)
    batch_size = 4096
    test_batch_size = 256
    train_loader = torch.utils.data.DataLoader(
        range(train_edge_label_index.size(1)),
        shuffle=True,
        batch_size=batch_size,
    )

    # Load model
    model = load_parameters(in_model_path).to(device)

    k = 20

    # Evaluate
    with torch.no_grad():
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


    # JSON schema
    report = {
        "precision": precision / total_examples,
        "recall": recall / total_examples,
    }

    # Save JSON
    save_metrics(report, out_json_path)


if __name__ == "__main__":
    validate(sys.argv[1], sys.argv[2])
