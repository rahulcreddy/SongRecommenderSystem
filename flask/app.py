from flask import Flask, request, render_template
#import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
#import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from artist_info import fetch_track_info
import os

app = Flask(__name__)

#model = pickle.load(open('model_v1.0.pkl', 'rb'))  # loading the model

# define the relative path to your data file
data_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'track_features.csv'))

df = pd.read_csv(data_file_path)

# define the features that you want to use for similarity calculation
features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

# create a new column in the dataframe with a string representation of the features
df['features_str'] = df[features].apply(lambda x: ' '.join(x.astype(str)), axis=1)

# create a CountVectorizer object to convert the features string into a matrix
count = CountVectorizer()
features_matrix = count.fit_transform(df['features_str'])

# calculate cosine similarity between all tracks
cosine_sim = cosine_similarity(features_matrix, features_matrix)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/recommend',methods=['POST'])

def recommend():

    track_id = request.form['track_id']
    # get the index of the track
    idx = df[df['track_title']==track_id].index[0]
    # get the cosine similarity scores of the track with all other tracks
    sim_scores = list(enumerate(cosine_sim[idx]))
    # sort the tracks based on the similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # get the top 6 similar tracks
    sim_scores = sim_scores[1:7]
    # get the track indices
    track_indices = [i[0] for i in sim_scores]
    # return the track names
    #top_track_ids = df['track_title'].iloc[track_indices].tolist()
    top_tracks = [df.loc[index,] for index in track_indices]
    top_tracks = pd.DataFrame(top_tracks)
    top_tracks = top_tracks.reset_index(drop = True)
    top_tracks = fetch_track_info.get_track_info(top_tracks)
    top_tracks = top_tracks[['track_id', 'track_title', 'artist_name', 'album_cover_url', 'track_url']]

    return render_template('recommend.html', top_tracks=top_tracks)

if __name__ == '__main__':
    app.run(debug=True)