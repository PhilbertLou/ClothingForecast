import requests, json, csv, ast
import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split

key = 'KEY'
location = 'New York'
response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}&units=metric')
#print(response.status_code)
content = response.content
#print(content)

dictver = content.decode("UTF-8")
weatherdata = ast.literal_eval(dictver)
print(weatherdata)
#print(weatherdata['main']['feels_like'])
#print(weatherdata['weather'][0]['main'])

weatherspots = {
    'Thunderstorm': 3,
    'Drizze': 4,
    'Rain': 5,
    'Snow': 6,
    'Clear': 7,
    'Cloudy': 8,
    'Mist': 9,
    'Smoke': 9,
    'Haze': 9,
    'Dust': 9,
    'Fog': 9,
    'Sand': 9,
    'Ash': 9,
    'Squall': 9,
    'Tornado': 9
}
weatherpart = [0.0, 0.0 ,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

weathercond = weatherspots[weatherdata['weather'][0]['main']]
weatherpart[weathercond] = 1
weatherpart[10] = weatherdata['main']['feels_like']

print(weatherpart)

"""
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
"""

clothes = []
with open("clothes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append(
            [float(cell) for cell in row[:13]]
        )
    clothes = data

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

#model.evaluate(testdata1, testdata2, verbose=2)

"""
outcome = False

predval = model.predict([[0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,33.58]])
if (predval > 0.5):
    outcome = True
else:
    outcome = False
"""
#print(clothes)
#print(outcome)

alldata = clothes
#print(alldata)

for i in range(len(alldata)):
    alldata[i] = alldata[i] + weatherpart

#print(alldata)

numTrues = []
stringTrues = []

for j in range(len(alldata)):
    outcome = False
    predval = model.predict([alldata[j]])
    if (predval > 0.5):
        outcome = True
    else:
        outcome = False

    if outcome:
        numTrues.append(alldata[j])

outfits = {
    0: 'Umbrella',
    1: 'Sunscreen',
    2: 'Snowpants',
    3: 'Dress',
    4: 'Tee',
    5: 'Long shirt',
    6: 'Shorts/skirt',
    7: 'Long pants',
    8: 'Breezy pants',
    9: 'Thin sweater',
    10: 'Thick sweater',
    11: 'Windbreaker',
    12: 'Winter coat'
}

for combo in numTrues:
    outfit = []
    spots = []
    for k in range(12):
        if combo[k] == 1:
            spots.append(k)
    for l in range(len(spots)):
        outfit.append(outfits[spots[l]])
    stringTrues.append(outfit)

print(stringTrues)

