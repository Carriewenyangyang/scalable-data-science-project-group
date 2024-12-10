import os
from math import floor

import numpy as np
import torch
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
abs_path = os.path.abspath(dir_path)


def get_data(out_dir="data"):
    # Make dir if necessary
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

def load_data(data_path, is_train=True):
    """Load data from disk.

    :param data_path: Path to data file.
    :type data_path: str
    :param is_train: Whether to load training or test data.
    :type is_train: bool
    :return: Tuple of data and labels.
    :rtype: tuple
    """
    if data_path is None:
        data_path = os.environ.get("FEDN_DATA_PATH", abs_path + "/data/Spotify")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    class Data:
        def __init__(self, train_adj, edge_label_index):
            self.train_adj = train_adj
            self.edge_index = torch.from_numpy(np.concatenate([train_adj, train_adj[[1, 0], :]], axis=1)).to(device)
            self.edge_label_index = torch.from_numpy(edge_label_index).to(device)

    #num_users = 100000
    num_users = 1000000

    train_adj = np.load(data_path + "/train_adj-0-99.npy")
    train_adj[1, :] += num_users
    test_adj = np.load(data_path + "/test_adj-0-99.npy")
    test_adj[1, :] += num_users

    data = Data(train_adj, test_adj)

    return data


if __name__ == "__main__":
    # Prepare data if not already done
    if not os.path.exists(abs_path + "/data/clients/1"):
        get_data()
