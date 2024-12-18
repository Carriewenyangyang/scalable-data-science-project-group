# Data processing

The Spotify Million Playlist Dataset (MPD) was used for the project. It can be downloaded from different sources, such as Kaggle. 
However, the data is available for download here: https://drive.google.com/drive/folders/19cT8svEXxUmpq5Q6n54RyrzS2kuS1j7H

The stats.info file available in the gitrepo contains information about the playlists, distribution of songs, etc.

The dataset is the result of work by Ching-Wei Chen, Paul Lamere, Markus Schedl, and Hamed Zamani. Recsys Challenge 2018: Automatic Music Playlist Continuation. In Proceedings of the 12th ACM Conference on Recommender Systems (RecSys ’18), 2018. < href="https://doi.org/10.1145/3240323.3240342">https://doi.org/10.1145/3240323.3240342</a>

The use of the dataset is subject to these terms: https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/challenge_rules

## Step 1: Repackaging the original dataset

First step of the data processing pipeline. This script reads the Spotify MPD dataset and repackages it into fewer packets of data. Each packet contains 10,000 playlists. Since the project will treat all playlists alike, it also reformats the data so that the key for each entry is the playlist id, pid. 

## Step 2: Reformatting data for the project

Second step in the data processing pipeline. This script reads the raw data from the 100 files created in step one, cleans it, and saves it in a more efficient format. 

The script creates a lookup table for the data, and creates an adjacency matrix for the data. For the adjeceny matrix, only ids for playlist and songs are useful which saves space. The adjacency matrix is split into 51 training datasets and one test dataset, since the goal is to run 51 federated clients. 

The training datasets are saved in subfolders, and then zipped for easier download on the clients. 

## Data packets used for this work

The repackaged and reformated data used for this work is available at:
https://drive.google.com/drive/folders/1kY71gk1gPtTIvmz1WuDq2KgWEUyGpdtO?usp=sharing
