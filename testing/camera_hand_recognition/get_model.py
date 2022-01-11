import os

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers import Dense, Flatten

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd

# Sklearn
from sklearn.model_selection import train_test_split  # Helps with organizing data for training
from sklearn.metrics import confusion_matrix  # Helps present results as a confusion-matrix

# We need to get all the paths for the images to later load them
image_paths = []

# Go through all the files and subdirectories inside a folder and save path to images inside list
for root, dirs, files in os.walk("RawData/Left", topdown=False):
    for name in files:
        path = os.path.join(root, name)
        if path.endswith("png"):  # We want only the images
            image_paths.append(path)

print(len(image_paths))  # If > 0, then a PNG image was loaded

X = []  # Image data
y = []  # Labels

# Loops through image_paths to load images and labels into arrays
for path in image_paths:
    category = os.path.basename(path)
    label = int(category.split("_")[-1][0])
    y.append(label)

    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converts into the correct colorspace (GRAY)

    X.append(img)

# Turn X and y into np.array to speed up train_test_split
X = np.array(X, dtype="uint8")
X = X.reshape(len(X), 180, 160, 1)  # Needed to reshape so CNN knows it's different images
y = np.array(y)

ts = 0.1  # Percentage of images that we want to use for testing. The rest is used for training.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ts, random_state=5)

model = Sequential()
model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(180, 160, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(3, activation='softmax'))


# Configures the model for training
model.compile(optimizer='adam', # Optimization routine, which tells the computer how to adjust the parameter values to minimize the loss function.
              loss='sparse_categorical_crossentropy', # Loss function, which tells us how bad our predictions are.
              metrics=['accuracy']) # List of metrics to be evaluated by the model during training and testing.

# Trains the model for a given number of epochs (iterations on a dataset) and validates it.
model.fit(X_train, y_train, epochs=2, batch_size=8, verbose=2, validation_split=1/9)


# Save entire model to a HDF5 file
model.save('models/Left/a_left_hand_model.h5')


def test_model(X_test, y_test):
    test_loss, test_acc = model.evaluate(X_test, y_test)

    print('Test accuracy: {:2.2f}%'.format(test_acc*100))


test_model(X_test, y_test)
