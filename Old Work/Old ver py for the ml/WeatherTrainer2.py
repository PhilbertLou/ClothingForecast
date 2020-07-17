import requests, json, csv, ast, os
import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split


def retrain(evidence, label):
    newmodel = tf.keras.models.Sequential()
    newmodel.add(tf.keras.layers.Dense(512, input_shape=(23,), activation="relu"))

    newmodel.add(tf.keras.layers.Dense(950, input_shape=(512,), activation="sigmoid"))
    newmodel.add(tf.keras.layers.Dropout(0.5))

    newmodel.add(tf.keras.layers.Dense(1, activation="sigmoid"))


    custom = tf.keras.optimizers.Adagrad(
        learning_rate=0.000001,
        initial_accumulator_value=1200000, #1200000
        epsilon=1e-07,
        name="Adagrad",
    )

    newmodel.compile(
        optimizer=custom,
        loss="binary_crossentropy",
        metrics=["Accuracy"]
    )

    newmodel.load_weights("testsaves/test6")

    newmodel.fit(evidence, label, epochs=3)

    newmodel.save_weights("testsaves/test6")
