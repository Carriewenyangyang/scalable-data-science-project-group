"""

Second step in the data processing pipeline. This script reads the raw data from the Spotify dataset, 
cleans it, and saves it in a more efficient format. The script also creates a lookup table for the data, 
and creates an adjacency matrix for the data. The adjacency matrix is split into 51 training datasets 
and one test dataset. The training datasets are saved in subfolders, and then zipped. The script also 
saves the test dataset as a numpy file.

Work by: Olle Hansson, with contributions from Christian Gustavsson.

NOTE:
- There has to be data in the 'data/dirty' folder for this script to work.

"""

import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import zipfile
import shutil
from tqdm import tqdm

np.random.seed(0)

def create_clean_data(path, nr_of_original_packets=None):

    # create dataframe from json files
    df = pd.DataFrame()

    if nr_of_original_packets is not None:
        #for i in range(nr_of_original_packets):
        for i in tqdm(range(nr_of_original_packets)):
            with open(path + str(i) + ".json", 'r') as file:
                loaded = json.load(file)
                playlists = {playlist['pid']: playlist for playlist in list(loaded.values())}
                df = pd.concat([df, pd.DataFrame(playlists).T], axis=0)
    else:
        path = path + "0.json"
        with open(path, 'r') as file:
            loaded = json.load(file)
            playlists = {playlist['pid']: playlist for playlist in list(loaded.values())}
            df = pd.concat([df, pd.DataFrame(playlists).T], axis=0)

    ## The original data is in the following format:
    #        "name": "relax",
    #        "collaborative": "false",
    #        "pid": 94,
    #        "modified_at": 1495324800,
    #        "num_tracks": 124,
    #        "num_albums": 112,
    #        "num_followers": 1,
    #        "tracks": [
    #            {
    #                "pos": 0,
    #                "artist_name": "James Bay",
    #                "track_uri": "spotify:track:13HVjjWUZFaWilh2QUJKsP",
    #                "artist_uri": "spotify:artist:4EzkuveR9pLvDVFNx6foYD",
    #                "track_name": "Let It Go",
    #                "album_uri": "spotify:album:5BxvswQSGWrBbVCdx6mFGO",
    #                "duration_ms": 260533,
    #                "album_name": "Chaos And The Calm"
    #            },
    #        ],
    #        "num_edits": 35,
    #        "duration_ms": 27578241,
    #        "num_artists": 97,
    #        "description": "chilllll out"

    # remove all columns except for pid and tracks
    df = df[["pid", "tracks"]]

    # remove all columns except for track uri, and remove spotify:track:
    df["tracks"] = df["tracks"].apply(lambda x: [track["track_uri"].split(":")[-1] for track in x])

    # remove duplicates in tracks
    df["tracks"] = df["tracks"].apply(lambda x: list(set(x)))

    # save to pickle
    if nr_of_original_packets is not None:
        save_path = "data/packet-0-" + str(nr_of_original_packets-1) + "-clean"
    else:
        save_path = "data/packet-0-clean"
    #df.to_pickle(save_path + ".pkl")
    #df.to_csv(save_path + ".csv")
    #df.to_json(save_path + ".json")
    df.to_parquet(save_path + ".parquet")
    
    return df

def create_lookuptable(data):

    df = pd.DataFrame(data)

    # unpack tracks
    df = df.explode("tracks").reset_index(drop=True)

    # rename columns
    df.columns = ["pid", "track"]

    # create tuple of pids for unique track
    df = df.groupby("track")["pid"].apply(tuple).reset_index()

    # add column for number of pids
    df["num_pids"] = df["pid"].apply(lambda x: len(x))

    # sort by number of pids
    df = df.sort_values("num_pids", ascending=False).reset_index(drop=True)
    print(df)

    # drop all rows with less than 3 pids
    df = df[df["num_pids"] > 5]

    return df

def create_adjacency_matrix(df, train_splits=1):

    # create adjacency matrix in coo format
    arr_list = []

    for i, pids in enumerate(df["pid"]):
        for pid in pids:
            arr_list.append((pid, i))

    adj_arr = np.array(arr_list)

    # sort by first row
    adj_arr = adj_arr[np.lexsort((adj_arr[:,1], adj_arr[:,0]))]

    # Generate random indices
    indices = np.random.permutation(adj_arr.shape[0])

    # Calculate the split point
    split_point = int(0.98 * adj_arr.shape[0])

    # Split the indices into two parts: 98% and 2%
    split_indices1, split_indices2 = indices[:split_point], indices[split_point:]

    # Use the indices to split the original array
    test_adj = adj_arr[split_indices2]

    # lexsort
    test_adj = test_adj[np.lexsort((test_adj[:,1], test_adj[:,0]))]

    # transpose
    test_adj = test_adj.T

    # Split into 51 training datasets, resulting in 34 x 112080 and 17 x 112079
    training_datasets = np.array_split(split_indices1, train_splits)

    main_folder_name = "data-processing/data/fedn-packets"
    if not os.path.exists(main_folder_name):
        os.makedirs(main_folder_name)
        print(f"Folder '{main_folder_name}' created.")
    else:
        print(f"Folder '{main_folder_name}' already exists.")

    # Now we save the data packets in subfolders
    for i in range(len(training_datasets)):
        temp_dataset = training_datasets[i]
        train_adj = adj_arr[temp_dataset]
        train_adj = train_adj[np.lexsort((train_adj[:,1], train_adj[:,0]))]
        train_adj = train_adj.T

        # Saving the training and test datasets in subfolder
        sub_folder_name = main_folder_name + "/packet-" + str(i+1)
        os.makedirs(sub_folder_name)
        np.save(sub_folder_name + "/train_adj-0-99.npy", train_adj)
        np.save(sub_folder_name + "/test_adj-0-99.npy", test_adj)
        
    # Zipping the subfolders, starting by ensuring that the main folder exists
    if not os.path.exists(main_folder_name):
       print(f"Error: The folder '{main_folder_name}' does not exist.")
       return
    
    # Iterate through subfolders
    for subfolder in os.listdir(main_folder_name):
       subfolder_path = os.path.join(main_folder_name, subfolder)
    
       # Only directories 
       if os.path.isdir(subfolder_path):
           zip_name = f"{subfolder}.zip"
           zip_path = os.path.join(main_folder_name, zip_name)
    
           try:
               # Create the zip file
               with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                   for root, _, files in os.walk(subfolder_path):
                       for file in files:
                           file_path = os.path.join(root, file)
                           arcname = os.path.relpath(file_path, subfolder_path)
                           zipf.write(file_path, arcname=arcname)
                           # print(f"Added '{file_path}' to '{zip_name}' as '{arcname}'.")
    
               print(f"Subfolder '{subfolder}' successfully zipped as '{zip_name}'.")
    
               # Remove the subfolder
               shutil.rmtree(subfolder_path)
               print(f"Subfolder '{subfolder}' removed.\n")
    
           except Exception as e:
               print(f"Error zipping/removing subfolder '{subfolder}': {e}")

    return train_adj, test_adj

def get_track_info(df, track_df_index):

    # get track uri
    track_uri = df["track"][track_df_index]

    # get track info from spotify
    link = "https://open.spotify.com/track/" + track_uri.split(":")[-1]
    
    return link

## MAIN PROGRAM:

nr_of_original_packets = 100 # The original amount of packets is 100 (the # of dirty files)
nr_of_client_datapackets = 51 # The amount of client data packets is 51 for our work (the # clients to use later on)

# create clean data. 
dirty_path = "data/dirty/packet-" 
clean_data = create_clean_data(dirty_path, nr_of_original_packets=nr_of_original_packets)

# load clean data
clean_path = "data-processing/data/packet-0-" + str(nr_of_original_packets-1) + "-clean"
clean_data = pd.read_parquet(clean_path + ".parquet")

# create dataframe
df = create_lookuptable(clean_data)
# print(df)

# save df to parquet
df.to_parquet("data-processing/data/lookuptable-0-" + str(nr_of_original_packets-1) + ".parquet")

# load df
df = pd.read_parquet("data-processing/data/lookuptable-0-" + str(nr_of_original_packets-1) + ".parquet")
# create adjacency matrix
train_adj, test_adj = create_adjacency_matrix(df, nr_of_client_datapackets)

# save adj_arr to npy
np.save("data-processing/data/train_adj-0-" + str(nr_of_original_packets-1) + ".npy", train_adj)
np.save("data-processing/data/test_adj-0-" + str(nr_of_original_packets-1) + ".npy", test_adj)

print("The preprocessing work is done!")

# The get_track_info() function can be used to get the track info from a track index in the dataframe.
