import requests, json, csv, ast
import tensorflow as tf
from tensorflow import keras
import WeatherTrainer2 as wt

from sklearn.model_selection import train_test_split

key = 'KEY'
location = 'New York'
model = tf.keras.models.Sequential()
def getweatherinfo():
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

    return weatherpart

def makeset(weatherpart):
    with open("clothes.csv") as f:
        reader = csv.reader(f)
        next(reader)

        data = []
        for row in reader:
            data.append(
                [float(cell) for cell in row[:12]]
            )
        clothes = data

    for i in range(len(clothes)):
        clothes[i] = clothes[i] + weatherpart
    return clothes

def makemodel():
    model.add(tf.keras.layers.Dense(512, input_shape=(23,), activation="relu"))

    model.add(tf.keras.layers.Dense(950, input_shape=(512,), activation="sigmoid"))
    model.add(tf.keras.layers.Dropout(0.5))

    model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    model.load_weights("testsaves/test6")

def predict(alldata):
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

    #for combo in stringTrues:
        #print(combo)

    for i, combo in enumerate(stringTrues):
        print(f'Combo {i+1}: {combo}')

    return numTrues, stringTrues

def getresults(numresults):
    badlist = []
    num = -1

    if len(numresults) == 0:
        numresults = getbackup()

    while num != 0:
        print("Enter which combo number you would like to remove \nEnter 0 to go to next step")
        num = int(input())
        if num == 0:
            break
        if len(numresults) >= num > 0:
            badlist.append(num-1)

    #print(badlist)

    print("Enter which combo number you would like to choose\nEnter 0 if none.")
    goodnum = int(input())-1
    if goodnum == -1:
        return getresults([])

    newdata1 = []
    newdata2 = []

    for i in range(len(badlist)):
        newdata1.append(numresults[badlist[i]])
        newdata2.append(0)

    newdata1.append(numresults[goodnum])
    newdata2.append(1)

    return newdata1, newdata2

def getbackup():
    global model
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(512, input_shape=(23,), activation="relu"))

    model.add(tf.keras.layers.Dense(950, input_shape=(512,), activation="sigmoid"))
    model.add(tf.keras.layers.Dropout(0.5))

    model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    model.load_weights("testsaves/test6b")
    numresults, stringresults = predict(alldata)

    print('Backup')
    return numresults

if __name__ == "__main__":
    weatherinfo = getweatherinfo()
    alldata = makeset(weatherinfo)
    while True:
        makemodel()
        numresults, stringresults = predict(alldata)
        trainX, trainy = getresults(numresults)
        #print(trainX)
        #print(trainy)
        wt.retrain(trainX, trainy)

#Consider what may happen if no results show up or the only results are bad results