import requests, json, csv
import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split



key = 'enter key here'
location = 'New York'
response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}&units=metric')
print(response.status_code)
print(response.content)

traindata1 = []
traindata2 = []
testdata1 = []
testdata2 = []

with open("Data2d.csv") as f:
    reader = csv.reader(f)
    print(next(reader))

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:24]],
            "label": 1 if row[24] == "TRUE" else 0
        })

    evidence = [row["evidence"] for row in data]
    labels = [row["label"] for row in data]
    """X_training, X_testing, y_training, y_testing = train_test_split(
        evidence, labels, test_size=0.4
    )"""

    traindata1 = evidence
    traindata2 = labels


    #print(X_training)
    #print(y_training)

with open("testdatad.csv") as f:
    reader = csv.reader(f)
    print(next(reader))

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


model.fit(traindata1, traindata2, epochs=20)

model.save_weights("./SavedData")

#model.fit(X_training, y_training, epochs=20)

#model.evaluate(X_testing, y_testing, verbose=2)

model.evaluate(testdata1, testdata2, verbose=2)

#model.summary()

#print(model.predict([[0,0,0,0,-20]]))
