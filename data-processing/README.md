# Data processing

For the project, the Spotify Million Playlist Dataset (MPD) was used. It can be downloaded from different sources, such as Kaggle: https://www.kaggle.com/datasets/himanshuwagh/spotify-million

The stats.info file available in the gitrepo contains information about the playlists, distribution of songs etc.

The dataset is the result of work by Ching-Wei Chen, Paul Lamere, Markus Schedl, and Hamed Zamani. Recsys Challenge 2018: Automatic Music Playlist Continuation. In Proceedings of the 12th ACM Conference on Recommender Systems (RecSys ’18), 2018.

The use of the dataset are subject to these terms: https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/challenge_rules


## Repackaging the original dataset

In its original form, MPD consits of 1,000 files where each file contain 1,000 playlists. Running repackaging-spotify-mpd.py repackages these data files into 100 files instead. Since the project will treat all playlists alike, it also reformats the data so that the key for each entry is the playlist id, pid. 

## Reformatting data for the project

