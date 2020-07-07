import requests, json, csv, ast, os
import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split

testdata1 = []
testdata2 = []

testdata1b = []
testdata2b = []

with open("testdataf.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:24]],
            "label": 1 if row[24] == "TRUE" else 0
        })

    evidence = [row["evidence"] for row in data]
    labels = [row["label"] for row in data]

    testdata1 = evidence
    testdata2 = labels

with open("testdatag.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:24]],
            "label": 1 if row[24] == "TRUE" else 0
        })

    evidence = [row["evidence"] for row in data]
    labels = [row["label"] for row in data]

    testdata1b = evidence
    testdata2b = labels


    #print(testdata1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(512, input_shape=(24,), activation="relu"))

model.add(tf.keras.layers.Dense(950, input_shape=(512,), activation="sigmoid"))
model.add(tf.keras.layers.Dropout(0.5))

model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

# 0.00041234, 0.00048253,0.00045226, 0.00042555
custom = tf.keras.optimizers.Adam(
    learning_rate=1000000,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-07,
    amsgrad=False,
    name="Adam"
)

custom2 = tf.keras.optimizers.Adagrad(
    learning_rate=0.000001,
    initial_accumulator_value=1200000,
    epsilon=1e-07,
    name="Adagrad",
)

model.compile(
    optimizer=custom2,
    loss="binary_crossentropy",
    metrics=["Accuracy"]
)

model.load_weights("testsaves/test2")

"""
checkpoint_path = "./SavedData1"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

model.fit(testdata1,
          testdata2,
          epochs=10,
          validation_data=(traindata1,traindata2),
          callbacks=[cp_callback]) #validation_data=(test_images,test_labels),
"""
#model.evaluate(testdata1, testdata2, verbose=2)

result = model.predict([testdata1[0]])
print(result)
bool = False
if result > 0.5:
    bool = True

print(bool)


#model.fit(testdata1, testdata2, epochs=5)

"""
result = model.predict([[0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,-19]])
print(result)
bool = False
if result > 0.5:
    bool = True

print(bool)

result = model.predict([[0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,-21]])
print(result)
bool = False
if result > 0.5:
    bool = True

print(bool)

result = model.predict([[0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,35]])
print(result)
bool = False
if result > 0.5:
    bool = True

print(bool)
"""

#model.fit(testdata1, testdata2, epochs=1)


result = model.predict([testdata1[0]])
print(result)
bool = False
if result > 0.5:
    bool = True

print(bool)
"""
result = model.predict([[0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,-19]])
print(result)
bool = False
if result > 0.5:
    bool = True

print(bool)

result = model.predict([[0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,-21]])
print(result)
bool = False
if result > 0.5:
    bool = True

print(bool)

result = model.predict([[0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,35]])
print(result)
bool = False
if result > 0.5:
    bool = True

print(bool)
"""
model.evaluate(testdata1b, testdata2b, verbose=2)
#model.save_weights("testsaves/test2")
