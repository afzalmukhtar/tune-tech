#!/bin/python3

# Load Other Files
import pickle
from .FeatureExtractor import FeatureExtractor
from .PathList import VARIABLES_PATH, COLUMN_ORDER, AUDIO_MODELS_PATH
from .secret import spotify_client_id, spotify_client_secret

# Data Formats
from collections import defaultdict
import pandas as pd

# Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SongAudio(FeatureExtractor):

    def __init__(self, SPOTIFY_API_ID_KEY, MODEL_PATHS):
        client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_API_ID_KEY[0], client_secret=SPOTIFY_API_ID_KEY[1])
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.audio_model = super().__load_model__(MODEL_PATHS)[0]
        self.columns_order = COLUMN_ORDER
        variables = pickle.load(open(VARIABLES_PATH, "rb"))
        self.scaler = variables['scaler_audio']
        self.audio_mood_map = variables['mapping_audio']

    
    def __get_data__(self, artist_name, song_name):
        data = defaultdict(dict)
        result = self.sp.search(f"{artist_name.lower()} {song_name.lower()}")['tracks']['items'][0]
        if result['type'] == 'track':
            meta = self.sp.track(result['id'])
            features =  self.sp.audio_features(result['id'])[0]
        
        # Meta data
        data['name'] = meta['name']
        data['album'] = meta['album']['name']
        data['artist'] = meta['album']['artists'][0]['name']
        data['id'] = meta['id']
        data['release_date'] = meta['album']['release_date']
        data['popularity'] = meta['popularity']
        data['album_art'] = meta['album']['images'][0]['url'] # Album art
        data['duration_ms'] = meta['duration_ms']
        
        
        
        # Features
        data['danceability']  = features['danceability']
        data['acousticness']  = features['acousticness']
        data['energy']  = features['energy']
        data['instrumentalness']  = features['instrumentalness']
        data['liveness']  = features['liveness']
        data['valence']  = features['valence']
        data['loudness']  = features['loudness']
        data['speechiness']  = features['speechiness']
        data['tempo']  = features['tempo']
        data['key']  = features['key']
        data['time_signature']  = features['time_signature']
        return data


    def __get_vectors__(self, data):
        data = data.iloc[:, 7:-2].values
        data = self.scaler.transform(data)
        return data
        

    def __analyse_mood__(self, vector):
        prediction = self.audio_model.predict(vector)
        prediction = self.audio_mood_map[prediction[0]]
        return prediction


    def get_audio_features(self, artist_name, song_name):
        result = self.__get_data__(artist_name, song_name)
        result = pd.DataFrame.from_dict(data=result, orient='index').T
        return result


    def get_mood(self, data):
        vector = self.__get_vectors__(data)
        prediction = self.__analyse_mood__(vector)
        return prediction


if __name__ == "__main__":
    paths = AUDIO_MODELS_PATH
    client_id = spotify_client_id
    client_secret = spotify_client_secret
    
    SPOTIFY_API_ID_KEY = [client_id, client_secret]
    Audio = SongAudio(SPOTIFY_API_ID_KEY, paths)
    artist_name = 'Bernard Fanning'
    song_name = 'Shelter For My Soul'
    result = Audio.get_audio_features(artist_name, song_name)
    print(Audio.get_mood(result))
