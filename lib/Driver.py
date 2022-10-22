from typing import Dict, List
from FaceEmotion import FaceEmotion
from SongLyrics import SongLyrics
from SongRecommender import SongRecommender
from SongAudio import SongAudio
from PathList import *
from secret import *
import pandas as pd

from os import listdir, path


class Driver:

    def __init__(self) -> None:
        self.FER = FaceEmotion(FRONT_FACE_CASCADE, FER_MODELS_PATH)
        self.Audio = SongAudio(SPOTIFY_API_ID_KEY, AUDIO_MODELS_PATH)
        self.Lyrics = SongLyrics(GENIUS_API_TOKEN, LYRICS_MODELS_PATH) # DETECT_LANGUAGE_API_TOKEN
        self.Recommender = SongRecommender()

    def get_face_emotion(self, image_path) -> List:
        return self.FER.analyse_mood(image_path)
    
    def get_song_data(self, song_name, artist_name) -> Dict:
        result = self.Audio.get_audio_features(artist_name, song_name)
        song_name, artist_name = result['name'][0], result['artist'][0]
        album_name, duration = result['album'][0], result['duration_ms'][0]
        album_art = result['album_art'][0] #Album art
        audio_mood = self.Audio.get_mood(result)
        audio_mood = audio_mood.lower()
        lyrical_mood = self.Lyrics.get_mood(self.Lyrics.get_song_lyrics(artist_name, song_name))
        lyrical_mood = lyrical_mood.lower()
        data = {'song' : song_name, 'artist' : artist_name, 
                'album' : album_name, 'album_art' : album_art, 
                'duration' : duration, 
                'audio_mood' : audio_mood, 'lyrics_mood' : lyrical_mood}
        return data


    def recommend_song(self, song_list, mood_list=None) -> List: # [chosen_mood, neutral]
        # Uncomment Next line for testing Recommendation Output
        # mood_list = ['happy', 'surprise']
        if mood_list == None:
            image_path = "media/images"
            image_path = path.join(image_path, sorted(listdir(image_path), reverse=True)[0])
            mood_list = self.get_face_emotion(image_path)
        
        song_list = pd.DataFrame.from_dict(song_list)
        recommendation = self.Recommender.get_song_recommendation(mood_list, song_list)[['song', 'artist']]
        recommendation = list(recommendation.itertuples())
        return recommendation



