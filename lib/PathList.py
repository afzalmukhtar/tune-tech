#!/bin/python3

VARIABLES_PATH = "./Models/variables.pickle"

# FaceEmotion Variables
FER_MODELS_PATH = ["./Models/FER_part_1.h5", "./Models/FER_part_2.dat"]
FRONT_FACE_CASCADE = "./Models/haarcascade_frontalface_default.xml"
TEST_IMAGE = "./Models/Test image.jpg"

# SongAudio Variables
COLUMN_ORDER = ['name', 'album', 'artist', 'id', 'release_date', 'popularity', 'duration_ms', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'valence', 'loudness', 'speechiness', 'tempo', 'key', 'time_signature']
AUDIO_MODELS_PATH = ["./Models/Audio_Mood.dat"]


# SongLyrics Variables
LYRICS_MODELS_PATH = ["./Models/Lyrics_Mood_part_1.dat", "./Models/Lyrics_Mood_part_2.h5", "./Models/Lyrics_Mood_part_3.h5"]

# SongRecommender Variables
SONG_LIST_PATH = "./Models/SongList.csv"