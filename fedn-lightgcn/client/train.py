import math
import os
import sys

import torch
from model import load_parameters, save_parameters

from data import load_data
from fedn.utils.helpers.helpers import save_metadata

from tqdm import tqdm

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(dir_path))


def train(in_model_path, out_model_path, data_path=None, batch_size=8192, epochs=1, lr=0.001):
    """Complete a model update.

    Load model paramters from in_model_path (managed by the FEDn client),
    perform a model update, and write updated paramters
    to out_model_path (picked up by the FEDn client).

    :param in_model_path: The path to the input model.
    :type in_model_path: str
    :param out_model_path: The path to save the output model to.
    :type out_model_path: str
    :param data_path: The path to the data file.
    :type data_path: str
    :param batch_size: The batch size to use.
    :type batch_size: int
    :param epochs: The number of epochs to train.
    :type epochs: int
    :param lr: The learning rate to use.
    :type lr: float
    """

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load data
    data = load_data(data_path)
    num_playlists = 1000000
    num_tracks = 857768
    
    train_adj = data.train_adj
    train_edge_label_index = torch.from_numpy(train_adj).to(device)
    batch_size = 4096
    train_loader = torch.utils.data.DataLoader(
        range(train_edge_label_index.size(1)),
        shuffle=True,
        batch_size=batch_size,
    )

    # Load parmeters and initialize model
    model = load_parameters(in_model_path).to(device)

    # Train
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
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

    # Metadata needed for aggregation server side
    metadata = {
        # num_examples are mandatory
        "num_examples": total_examples, # maybe wrong
        "batch_size": batch_size,
        "epochs": epochs,
        "lr": lr,
        "loss": total_loss / total_examples,
    }

    # Save JSON metadata file (mandatory)
    save_metadata(metadata, out_model_path)

    # Save model update (mandatory)
    save_parameters(model, out_model_path)


if __name__ == "__main__":
    train(sys.argv[1], sys.argv[2])
