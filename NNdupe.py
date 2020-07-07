import requests, json, csv, ast
import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split

model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Dense(512, input_shape=(24,), activation="relu"))
#model.add(tf.keras.layers.Dropout(0.3))

model.add(tf.keras.layers.Dense(950, input_shape=(512,), activation="sigmoid"))
model.add(tf.keras.layers.Dropout(0.5))

#model.add(tf.keras.layers.Dense(900, activation="sigmoid"))
#model.add(tf.keras.layers.Dropout(0.5))

#model.add(tf.keras.layers.Dense(1000, activation="sigmoid"))
#model.add(tf.keras.layers.Dropout(0.5))

model.add(tf.keras.layers.Dense(1, activation="sigmoid"))


model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.load_weights("WeatherWear/Weatherwear1a") #5g is the base for this final ver
model.save_weights("WeatherWear/Weatherwear1b")