#!/bin/python3

# Load Other Files
from lib.PathList import VARIABLES_PATH

# Data Format
import pandas as pd
import pickle


class SongRecommender:

    def __init__(self):
        self.total = 5
        self.recommender_mapping = pickle.load(open(VARIABLES_PATH, "rb"))['mapping_recommender']
        
    
    def __get_angry__(self, percent):
        count = round(percent * self.total)
        data = self.song_data[self.song_data['lyrics_mood'] == 'angry']
        data = data.append(self.song_data[self.song_data['audio_mood'] == 'calm'])
        length = len(data.index)
        if length >= count:
            return data.sample(n=count)
        if length:
            return data.sample(n=length)


    def __get_energetic__(self, percent):
        count = round(percent * self.total)
        data = self.song_data[self.song_data['lyrics_mood'] == 'angry']
        data = data.append(self.song_data[self.song_data['audio_mood'] == 'energetic'])
        length = len(data.index)
        if length >= count:
            return data.sample(n=count)
        if length:
            return data.sample(n=length)


    def __get_happy__(self, percent):
        count = round(percent * self.total)
        data = self.song_data[self.song_data['audio_mood'] == 'happy']
        data = data.append(self.song_data[self.song_data['lyrics_mood'] == 'happy'])
        length = len(data.index)
        if length >= count:
            return data.sample(n=count)
        if length:
            return data.sample(n=length)


    def __get_relaxed__(self, percent):
        count = round(percent * self.total)
        data = self.song_data[self.song_data['audio_mood'] == 'calm']
        data = self.song_data[self.song_data['lyrics_mood'] == 'relaxed']
        length = len(data.index)
        if length >= count:
            return data.sample(n=count)
        if length:
            return data.sample(n=length)


    def __get_sad__(self, percent):
        count = round(percent * self.total)
        data = self.song_data[self.song_data['audio_mood'] == 'sad']
        data = self.song_data[self.song_data['lyrics_mood'] == 'sad']
        length = len(data.index)
        if length >= count:
            return data.sample(n=count)
        if length:
            return data.sample(n=length)


    def __get_songs__(self, percent):


        music_list = pd.DataFrame()
        music_list = music_list.append(self.__get_angry__(percent=percent['angry']))
        music_list = music_list.append(self.__get_energetic__(percent=percent['energetic']))
        music_list = music_list.append(self.__get_happy__(percent=percent['happy']))
        music_list = music_list.append(self.__get_relaxed__(percent=percent['relaxed']))
        music_list = music_list.append(self.__get_sad__(percent=percent['sad']))
        music_list = music_list.drop_duplicates()
        
        replace = True if self.song_data.shape[0] < self.total else False
        
        index = set(music_list.index)
        remaining = list(set(self.song_data.index).difference(index))
        remaining = remaining if len(remaining) else list(index)
        
        data = self.song_data.iloc[remaining]
        count = len(index)

        if count < self.total:
            music_list = music_list.append(data.sample(n=self.total - count, replace=replace))
        if count > self.total:
            music_list = music_list.sample(n=self.total)
        return music_list


    def get_song_recommendation(self, moods, songs_list):
        
        percentages = self.recommender_mapping[(moods[0], moods[1])]
        # Add part to extract from lyrical or audio based on moods
        self.song_data = songs_list

        music_list = self.__get_songs__(percentages)
        return music_list

    
if __name__ == "__main__":

    from lib.PathList import SONG_LIST_PATH
    songs = pd.read_csv(SONG_LIST_PATH)
    songs['Mood'] = songs['Mood'].apply(lambda x : x.lower())
    songs['audio_mood'] = songs['Mood']
    songs['lyrics_mood'] = songs['Mood'].sample(frac = 1)
    songs.drop(columns=['Mood'], inplace=True)
    Recommender = SongRecommender()
    print(Recommender.get_song_recommendation(['happy', 'neutral'], songs), sep="\n")
