import requests, json, csv
import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split

key = '052d065281c185db20f824d4b2ecf002'
location = 'New York'
response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}&units=metric')
print(response.status_code)
print(response.content)


testdata1 = []
testdata2 = []

with open("testdatae.csv") as f:
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

model.load_weights("./SavedData")

model.evaluate(testdata1, testdata2, verbose=2)

outcome = False

predval = model.predict([[0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,33.58]])
if (predval > 0.5):
    outcome = True
else:
    outcome = False


print(outcome)