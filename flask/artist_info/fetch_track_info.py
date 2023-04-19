import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os

# Get the current working directory
cwd = os.getcwd()
# create a relative path to the data file
data_file = os.path.join(cwd, 'client_cred', 'creds.txt')

# open the text file
with open(data_file, 'r') as f:
    cid = f.readline().strip()
    secret = f.readline().strip()

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_album_cover_url(track_id):
    album_cover_url = sp.tracks([track_id])['tracks'][0]['album']['images'][1]['url']
    return album_cover_url

def get_track_url(track_id):
    track_url = sp.tracks([track_id])['tracks'][0]['external_urls']['spotify']
    return track_url

def get_track_info(track_dataframe):
    track_dataframe['album_cover_url'] = track_dataframe['track_id'].apply(get_album_cover_url)
    track_dataframe['track_url'] = track_dataframe['track_id'].apply(get_track_url)
    return track_dataframe