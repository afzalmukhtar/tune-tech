#!/bin/python3

# Load Other Files
from .FeatureExtractor import FeatureExtractor
import pickle

# Data Format
import numpy as np
from collections import Counter

# Image
import cv2 as cv
# from keras.preprocessing import image
from tensorflow.keras.preprocessing import image

# Keras
from keras.models import load_model

from .PathList import VARIABLES_PATH, FER_MODELS_PATH, FRONT_FACE_CASCADE

class FaceEmotion(FeatureExtractor):

    def __init__(self, cascade_path, model_paths):
        self.face_cascade = cv.CascadeClassifier(cascade_path)
        # self.model_1, self.model_2 = self.__load_model__(model_paths)
        self.model_1 = super().__load_model__(model_paths)[0]
        # self.model_1 = Model(self.model_1.input, self.model_1.get_layer('dense_6').output)


        variables = pickle.load(open(VARIABLES_PATH, "rb"))
        self.scaler = variables['scaler_fer']
        self.mapping_fer_mood = variables['mapping_fer']


    # def __load_model__(self, paths):
    #     models = []
    #     for i in paths:
    #         if 'h5' in i.split(".")[-1]:
    #             models.append(load_model(i))
    #         else:
    #             models.append(pickle.load(open(i, 'rb')))
    #     return models


    def __get_vectors__(self, data):
        img_pixels = image.img_to_array(data)
        img_pixels = np.expand_dims(img_pixels, axis = 0)
        img_pixels =  img_pixels / 255.0
        return img_pixels
        # return self.scaler.transform(data)
    

    def __predict_mood__(self, image):
        prediction = self.model_1.predict(image)
        # prediction = self.__get_vectors__(prediction)
        # prediction = self.model_2.predict(prediction)
        return prediction.argmax(axis=1)
    

    def __get_crowd_mood__(self, img):
        original_image = cv.imread(img)
#         print(original_image)
        # cv2_imshow(original_image)
        # cv.imshow("Original Image", original_image)
        grayscale_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
        detected_faces = self.face_cascade.detectMultiScale(grayscale_image, 1.03, 25)
    
        prediction = []
        for (column, row, width, height) in detected_faces:
            # cv.rectangle(original_image, (column, row), (column + width, row + height), (0, 255, 0), 2)
            try:
                gray_image = grayscale_image[row:row+width,column:column+height]#cropping region of interest i.e. face area from  image
                gray_image=cv.resize(gray_image, (48,48))
                # cv2_imshow(gray_image)
                # img_pixels = image.img_to_array(gray_image)
                # img_pixels = np.expand_dims(img_pixels, axis = 0)
                # img_pixels =  img_pixels / 255.0
                img_pixels = self.__get_vectors__(gray_image)
                
                # print(img_pixels.shape)
                prediction.append(self.__predict_mood__(img_pixels)[0])

            except Exception as e:
                print(e)     
        return prediction


    def analyse_mood(self, image_path):
        
        predictions = self.__get_crowd_mood__(image_path)
        final_preds = [i[0] for i in Counter([self.mapping_fer_mood[i] for i in predictions]).most_common(2)]
        # print(final_preds)
        return final_preds

if __name__ == "__main__":
    paths = FER_MODELS_PATH
    cascade_path = FRONT_FACE_CASCADE
    FER = FaceEmotion(cascade_path, paths)
    
    from .PathList import TEST_IMAGE
    x = FER.analyse_mood(TEST_IMAGE) # Give path of Test Image
    print(x)