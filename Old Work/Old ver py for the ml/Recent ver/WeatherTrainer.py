import requests, json, csv, ast, os
import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split


def retrain(evidence, label):
    newmodel = tf.keras.models.Sequential()
    newmodel.add(tf.keras.layers.Dense(512, input_shape=(24,), activation="relu"))

    newmodel.add(tf.keras.layers.Dense(950, input_shape=(512,), activation="sigmoid"))
    newmodel.add(tf.keras.layers.Dropout(0.5))

    newmodel.add(tf.keras.layers.Dense(1, activation="sigmoid"))


    custom = tf.keras.optimizers.Adagrad(
        learning_rate=0.5,
        initial_accumulator_value=12, #1200000
        epsilon=1e-07,
        name="Adagrad",
    )

    custom2 = tf.keras.optimizers.Adam(
        learning_rate=0.001,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-07,
        amsgrad=False,
        name="Adam",
    )

    newmodel.compile(
        optimizer=custom2,
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    newmodel.load_weights("testsaves/test5i") #7d for winter weighting, leaving 5h alone for now starting anew with 5i

    newmodel.fit(evidence, label, epochs=5)

    newmodel.save_weights("testsaves/test5i")
