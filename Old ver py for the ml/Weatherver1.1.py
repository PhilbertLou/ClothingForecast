import requests, json, csv, ast
import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split

key = 'KEY'
location = 'Phoenix'
response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}&units=metric')
content = response.content

dictver = content.decode("UTF-8")
weatherdata = ast.literal_eval(dictver)
print(weatherdata)

weatherspots = {
    'Thunderstorm': 3,
    'Drizze': 4,
    'Rain': 5,
    'Snow': 6,
    'Clear': 7,
    'Clouds': 8,
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

model.load_weights("testsaves/test1")

alldata = clothes

for i in range(len(alldata)):
    alldata[i] = alldata[i] + weatherpart

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

