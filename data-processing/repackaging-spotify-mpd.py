"""

First step of the data processing pipeline. This script reads the Spotify MPD dataset and 
repackages it into smaller packets of data. Each packet contains 100 playlists. The 
packets are saved as JSON files in the 'fedn-packets' directory.

Instead of downloading the entire dataset, you can directly download the packets crated by
this script. An instruction is available in the README.md file. Strongly recommended.

NOTE:
If you want to run this scipt, you need to download the Spotify MPD dataset from Kaggle. 
Place the set mpd.slice.XX slice files in the 'data/spotify' directory before running this script.

Work by: Christian

"""

import json
from tqdm import tqdm
import numpy as np


playlists = 1000000 # m number of playlists in dataset
packets = 100       # n number of simulated users, generating n packets of data

# Creates intervals that matches file names
intervals = np.zeros((2,1000), dtype=int)
for i in range(1000):
    low = i * 1000
    high = (i+1)* 1000 - 1
    intervals[0][i] = low
    intervals[1][i] = high

# Repackages the data into packets of 100 set of 10,000 playlists    
for p in tqdm(range(100)):
    selected = intervals[:,p*10:(p+1)*10]

    first = True
    packets = {}

    for i in range(10):
        load_path = f"data/spotify/mpd.slice.{selected[0,i]}-{selected[1,i]}.json" # <-- This needs to be downloaded from Kaggle
        with open(load_path, 'r') as file:
            loaded = json.load(file)
            playlists = {playlist['pid']: playlist for playlist in loaded["playlists"]}

        packets.update(playlists)

    save_path = f"data-processing/data/dirty/packet-{p}.json"

    with open(save_path, "w") as outfile:
        json.dump(packets,outfile)            

