#!/bin/python3

# Load Other Files
import pickle
import traceback
from FeatureExtractor import FeatureExtractor
from PathList import VARIABLES_PATH, LYRICS_MODELS_PATH
from secret import GENIUS_API_TOKEN #,  detectlanguage_api_token
from time import sleep

# String Operations
import re
import string
import ftfy
import contractions

# Language Detection
import pycld2 as cld2
import detectlanguage

# Translator
from deep_translator import GoogleTranslator

# NLTK and SPACY
import nltk


from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import spacy

# Web Elements
import requests
from bs4 import BeautifulSoup

# Math Operation
from scipy.stats import mode





class SongLyrics(FeatureExtractor):

    def __init__(self, GENIUS_API_TOKEN, MODEL_PATHS, DETECT_LANGUAGE_API=None, PRINT=False):
        self.GENIUS_API_TOKEN = GENIUS_API_TOKEN
        detectlanguage.configuration.api_key = DETECT_LANGUAGE_API
        self.PRINT = PRINT
        self.last_song = None
        self.last_artist = None
    
        self.model_1, self.model_2, self.model_3  = super().__load_model__(MODEL_PATHS)
        self.splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()
        self.lemmatizer = WordNetLemmatizer()
        self.nlp_spacy = spacy.load("en_core_web_lg")
        variables = pickle.load(open(VARIABLES_PATH, "rb"))
        self.scaler = variables['scaler_lyrics']
        self.lyrics_mood_map = variables['mapping_lyrics']
        
        # POS Tag Mapping
        self.mapping = {'J' : wordnet.ADJ, 'V' : wordnet.VERB, 'N' : wordnet.NOUN, 'R' : wordnet.ADV}

        if not DETECT_LANGUAGE_API:
            print("WARN: DetectLanguage will not be used...\n")
        

    def __request_song_url__(self, artist_name, song_name):
        base_url = 'https://api.genius.com'
        headers = {'Authorization': 'Bearer ' + self.GENIUS_API_TOKEN}
        search_url = base_url + '/search?'
        data = {'q': artist_name + ' ' + song_name}
        response = requests.get(search_url, data=data, headers=headers).json()
        # pprint(response)
        return response


    def __get_data__(self, url):
        page = requests.get(url)
        if self.PRINT:
            print(url)
        # sleep(2)
        html = BeautifulSoup(page.text, 'html.parser')
        
        lyrics = [i.get_text('|/n|') for i in html.find_all('div', attrs={'class': re.compile('Lyrics__Container-sc-*')})] # class_='Lyrics_Container-sc-1ynbvzw-6 krDVEH'
        sleep(0.5)
        lyrics = " ".join(lyrics)
        
        if not len(lyrics):
            lyrics = "instrumental"
            return lyrics
        
        # remove identifiers like chorus, verse, etc
        lyrics = re.sub(' +', ' ', re.sub(r'\[.*?\]', '', lyrics))
        lyrics = re.sub('(\|/n\|)+', '\n', lyrics)
        
        # print(lyrics)

        lyrics = self.__clean_data__(lyrics)

        return lyrics
    

    def __get_vectors__(self, lyrics):
        tokens = [self.tokenizer.tokenize(sent) for sent in self.splitter.tokenize(lyrics)]
        pos_tokens = [nltk.pos_tag(token) for token in tokens]
        pos_tokens = [[self.lemmatizer.lemmatize(word, self.mapping.get(pos_tag[0], wordnet.NOUN)) for (word, pos_tag) in pos] for pos in pos_tokens]
        pos_tokens = " ".join(pos_tokens[0])
        vector = self.nlp_spacy(pos_tokens).vector
        return vector


    def __detect_lang__(self, text, debug=False):

        text = text.strip().split("\n")
        languages_detected = set()
        try:
            # Using API
            languages_detected = set(dict(*filter(lambda x : x['isReliable'], i))['language'] for i in detectlanguage.detect(text))
        except (Exception, detectlanguage.DetectLanguageError) as e:
            if debug:
                print(f"ERROR: {e}")
                print(f"Not found using API. Trying cld2...")
            for i in text:
                cld2_detect = cld2.detect(i,  returnVectors=True, bestEffort=True)[-1]
                if cld2_detect != tuple():
                    languages_detected.add(cld2_detect[0][3])

        finally:
            languages_detected = list(filter(lambda x : x != 'un' and x != 'en', languages_detected))
            if languages_detected == list():
                languages_detected = 'auto'
        return languages_detected    


    def __translate_language__(self, text, src, debug=False):

        translated_text = []
        line_no = 0
        for line in text.split("\n"):
            if debug:
                print(f"Line Number: {line_no}\tLine: {line}")
                line_no += 1

            try:
                if isinstance(src, list):
                    for i in src:
                        line = GoogleTranslator(source=i, target='english').translate(line)
                else:
                    line = GoogleTranslator(source=src, target='english').translate(line)
            except Exception as e:
                if debug:
                    print(f"ERROR OCCURRED: {e}")
            finally:
                translated_text.append(line)
        
        return "\n".join(filter(None, translated_text))


    def __clean_data__(self, lyrics):
        
        lyrics = ftfy.fix_text(lyrics)
        src = self.__detect_lang__(lyrics)
        lyrics = self.__translate_language__(lyrics, src)
        lyrics = contractions.fix(lyrics) # Expand contractions
        
        non_word_char = set([i for i in set(lyrics) if not i.isalpha() and i != " "])
        non_word_char.update(set([str(i) for i in range(0, 10)]))
        non_word_char.update(set(string.punctuation))

        lyrics = lyrics.strip().lower().replace("\n", " ").replace("\r", " ") # Replace Newlines and carriage returns 
        lyrics = re.sub('\[.*?\]', '', re.sub('\{.*?\}', '', lyrics)) # Remove stuff inside brackets [] and {}
        lyrics = re.sub(r'\(\b(.+)(\s+\1\b)+\)', "", lyrics) # Stuff within ()
        
        for pattern in set([i for i in re.findall("\(.*?\)", lyrics) if len(i) <= 100]): # Stuff within () less than or 100 characters
            lyrics = lyrics.replace(pattern, " ")
        
        lyrics = " ".join([i for i in lyrics.split() if ":" not in i]) # Replace stuff like Baby: Cheerleader: or Baby :
        lyrics = lyrics.replace("-", " ") # Stuff like Oooh-oh-oh or c-c-c-c-come.
        
        for i in non_word_char:
            lyrics = lyrics.replace(i, "") # Remove other special characters and punctuations
        lyrics = " ".join([i for i in lyrics.split() if len(set(i)) > 1 and i != "a" and i != "an" and i != "the"])

        return lyrics


    def __analyse_mood__(self, lyrics):
        vector = self.__get_vectors__(lyrics)
        vector = vector.reshape(1, -1)
        vector = self.scaler.transform(vector)
        y_pred_1, y_pred_2, y_pred_3 = self.model_1.predict(vector).flatten().argmax(), self.model_2.predict(vector).flatten().argmax(), self.model_3.predict(vector).flatten().argmax()
        return y_pred_1, y_pred_2, y_pred_3


    def get_song_lyrics(self, artist_name, song_name):
        if self.PRINT:
            print(f"Song: {song_name} \nArtist: {artist_name}", "_"*50, sep='\n')
            
        self.last_song, self.last_artist = song_name, artist_name
        lyrics = "instrumental"
        response = self.__request_song_url__(artist_name, song_name)
        # print(response)
        
        try:
            song_url = response['response']['hits'][0]['result']['url']
            # print(song_url)
            lyrics = self.__get_data__(song_url)
        except Exception as e:
            print(f"\nError raised: {e}\nThe Song Lyrics doesn't exist\nArtist: {self.last_artist}\tSong: {self.last_song}")
            traceback.print_tb(e.__traceback__)
        # print(lyrics)
        return lyrics

    
    def get_mood(self, lyrics):
        if lyrics == "instrumental":
            return "neutral"
        y_pred_1, y_pred_2, y_pred_3 = self.__analyse_mood__(lyrics)
        final_pred = mode([y_pred_1, y_pred_2, y_pred_3]).mode[0]
        mood = self.lyrics_mood_map[final_pred]
        return mood

if __name__ == "__main__":
    paths = LYRICS_MODELS_PATH

    # DETECT_LANGUAGE_API = detectlanguage_api_token
    Lyrics = SongLyrics(GENIUS_API_TOKEN, paths, 
                        # PRINT=True,
                        # DETECT_LANGUAGE_API
                        )
    lyrics = Lyrics.get_song_lyrics('Bernard Fanning', 'Shelter For My Soul')
    print(lyrics)
    print(Lyrics.get_mood(lyrics))
    print(Lyrics.get_mood(Lyrics.get_song_lyrics('Forbidden Voices', 'Martin Garrix')))