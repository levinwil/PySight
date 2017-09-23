import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, load_model
from keras.layers import Dropout, Flatten, Dense, Convolution2D, MaxPooling2D, Activation
from keras import applications
from keras.utils.np_utils import to_categorical
import os
import matplotlib.pyplot as plt
import argparse
from keras import backend as K
import urllib, cStringIO
from PIL import Image
import time
import cv2

'''Load Theano backend so it can be used on Raspi'''
def set_keras_backend(backend):

    if K.backend() != backend:
        os.environ['KERAS_BACKEND'] = backend
        reload(K)
        assert K.backend() == backend

set_keras_backend("theano")



class Image_MLP(object):

    def __init__(self,
                 img_width = 640,
                 img_height = 480,
                 model_path = None):
        self.img_width = img_width / 10
        self.img_height = img_height / 10
        if model_path != None:
            self.set_model(model_path)
        else:
            self.model = None

    '''sets the model to the model_path'''
    def set_model(self,
                  model_path):
        self.model = load_model(model_path)

    '''saves the model at the model_path'''
    def save_model(self,
                   save_path = 'saved_models/MLP_model.h5'):
        self.model.save(save_path)

    '''fits the model to the data in data_dir'''
    def fit(self,
            data_dir = './data',
            batch_size = 16,
            epochs = 50):

        train_data_dir = data_dir + '/train/'
        validation_data_dir = data_dir + '/validation/'

        train_labels = []
        for filename in os.listdir(train_data_dir + "Car/"):
            train_labels.append(1)
        for filename in os.listdir(train_data_dir + "No_Car/"):
            train_labels.append(0)
        train_labels = to_categorical(train_labels[0: \
        batch_size * int(len(train_labels) / batch_size)])
        nb_train_samples = len(train_labels)

        datagen = ImageDataGenerator(rescale=1. / 255)

        # build the VGG16 network
        model = applications.VGG16(include_top=False,
                                   weights='imagenet')

        generator = datagen.flow_from_directory(
            train_data_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=batch_size,
            class_mode=None,
            shuffle=False)
        train_data = model.predict_generator(
            generator,
            nb_train_samples / batch_size)

        validation_labels = []
        for filename in os.listdir(validation_data_dir + "Car/"):
            validation_labels.append(1)
        for filename in os.listdir(validation_data_dir + "No_Car/"):
            validation_labels.append(0)
        validation_labels = to_categorical(validation_labels[0: \
        batch_size * int(len(validation_labels) / batch_size)])
        nb_validation_samples = len(validation_labels)

        generator = datagen.flow_from_directory(
            validation_data_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=batch_size,
            class_mode=None,
            shuffle=False)
        validation_data = model.predict_generator(
            generator,
            nb_validation_samples / batch_size)


        # Define the transfer layer that we will be training
        model = Sequential()
        model.add(Flatten(input_shape=(train_data.shape[1:])))
        model.add(Dense(256,
                        activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(2,
                        activation='sigmoid'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='adamax',
                      metrics=["accuracy"])


        model.fit(train_data,
                               train_labels,
                               epochs=epochs,
                               batch_size=batch_size,
                               validation_data=(validation_data, validation_labels))
        self.model = model


    '''takes a picture, saves it to the test_data_dir, then predicts all the images
    in that directory'''
    def predict(self,
                take_picture,
                test_data_dir="./data/test",
                batch_size = 1):
        if self.model == None:
            raise ValueError("Please fit model or load model before prediction")
        else:
            if take_picture:
                fileName = test_data_dir + "/test/" + str(int(time.time())) + ".jpg"
                cap = cv2.VideoCapture(0)
                for _ in range(10):
                    _, img = cap.read()
                cv2.imwrite(fileName, img)
            nb_test_samples = 0
            for filename in os.listdir(test_data_dir + "/test/"):
                nb_test_samples += 1
            nb_test_samples = batch_size * int(nb_test_samples / \
            batch_size)

            #produce features from VGG16
            m = applications.VGG16(include_top=False,
                                   weights='imagenet')
            datagen = ImageDataGenerator(rescale=1. / 255)
            generator = datagen.flow_from_directory(
                test_data_dir,
                target_size=(self.img_width, self.img_height),
                batch_size=batch_size,
                class_mode=None,
                shuffle=False)
            filenames = generator.filenames
            test_data = m.predict_generator(
                generator,
                nb_test_samples / batch_size)

            #classify those features
            result = self.model.predict(test_data)
            predicted_class = np.argmax(result,
                                        axis=1)
            result_string = ""
            for i in range(len(filenames)):
                classify = ""
                if predicted_class[i] == 0:
                    classify = "NO "
                result_string += classify + "car" + "\n"
            return result_string
