import tensorflow as tf

#This function duplicates a the weights for a model
def dupe(savepath):

    #The original NN is made
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(512, input_shape=(24,), activation="relu"))
    model.add(tf.keras.layers.Dense(950, input_shape=(512,), activation="sigmoid"))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(1, activation="sigmoid"))
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    #The original weights are loaded then saved elsewhere
    model.load_weights("environment/Userdata/Originaldata/Weatherwear1original")
    model.save_weights(savepath)
