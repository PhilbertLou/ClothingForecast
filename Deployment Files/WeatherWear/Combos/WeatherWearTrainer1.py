#Import necessary modules
import requests, json, csv, ast, os
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

#This function makes a model with the same specifications as the other one and updates it
def retrain(evidence, label, request):
    newmodel = tf.keras.models.Sequential()
    newmodel.add(tf.keras.layers.Dense(512, input_shape=(24,), activation="relu"))

    newmodel.add(tf.keras.layers.Dense(950, input_shape=(512,), activation="sigmoid"))
    newmodel.add(tf.keras.layers.Dropout(0.5))

    newmodel.add(tf.keras.layers.Dense(1, activation="sigmoid"))

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

    #The old model will experience more training and will be updated
    newmodel.load_weights(f"environment/Userdata/{request.user.username}/{request.user.username}")
    newmodel.fit(evidence, label, epochs=5)
    newmodel.save_weights(f"environment/Userdata/{request.user.username}/{request.user.username}")
