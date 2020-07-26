from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import WeatherWear as ww
import tensorflow as tf
import requests, ast
from users.models import UserProfile

valuedic = {}
siteinfo = {}
key = 'key'

#This function will generate the homepage/dashboard for the logged in user
def index(request, username):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    #This will get weather informaiton to display about the logged in user
    entries = UserProfile.objects.filter(user=request.user)
    entry = entries.first()
    city = entry.city
    country = entry.country
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={key}&units=metric')
    content = response.content
    dictver = content.decode("UTF-8")
    weatherdata = ast.literal_eval(dictver)
    weather = [weatherdata['main']['feels_like'],weatherdata['weather'][0]['main'], weatherdata['name'], weatherdata['sys']['country']]

    #These function calls will get information to feed into the machine to predict what to wear
    weatherinfo = ww.getweatherinfo(request)
    alldata = ww.makeset(weatherinfo)
    ww.makemodel(request)
    numresults, stringresults = ww.predict(alldata)

    #If no results happen, general recommendations will be given
    if len(numresults) == 0:
        numresults, stringresults = ww.getbackup(alldata)
        ww.restartmodel(request)

    #This value is stored and will be used later
    valuedic[request.user.username] = numresults
    siteinfo[request.user.username] = (stringresults,weather)

    #The NN is cleared and results are passed into the html file
    ww.model = tf.keras.models.Sequential()
    tf.keras.backend.clear_session()
    return render(request, 'Combos/index.html', {
            'clothes': stringresults,
            'weatherinfo': weather
        })

#This function handles removing certain combinations
def remove(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        #Bad items and all items are retrieved and will be used
        baditems = request.POST.getlist('want')
        allitems = valuedic[request.user.username]

        #These two lists are made to store the indicies of the good combos and bad combos
        goodlist = []
        badlist = []

        #The two lists are filled based on the data from the form
        for num in baditems:
            badlist.append(int(num)-1)
        for i in range(len(allitems)):
            if i not in badlist:
                goodlist.append(i)

        #Data is transferred from the two lists into one list and their corresponding number (1 or 0) is stored in the other
        newdata1 = []
        newdata2 = []
        for i in range(len(badlist)):
            newdata1.append(allitems[badlist[i]])
            newdata2.append(0)
        for i in range(len(goodlist)):
            newdata1.append(allitems[goodlist[i]])
            newdata2.append(1)

        #The retrain function is called and then the user will be taken back to the homepage
        ww.wt.retrain(newdata1, newdata2, request)
        return HttpResponseRedirect(reverse("index"))

#This function is similar to index but instead it will go straight to the backup options
def getbackup(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":

        entries = UserProfile.objects.filter(user=request.user)
        entry = entries.first()
        city = entry.city
        country = entry.country
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={key}&units=metric')
        content = response.content
        dictver = content.decode("UTF-8")
        weatherdata = ast.literal_eval(dictver)

        weather = [weatherdata['main']['feels_like'],weatherdata['weather'][0]['main'], weatherdata['name'], weatherdata['sys']['country']]
        weatherinfo = ww.getweatherinfo(request)
        alldata = ww.makeset(weatherinfo)
        ww.makemodel(request)

        numresults, stringresults = ww.getbackup(alldata)
        ww.restartmodel(request)

        valuedic[request.user.username] = numresults
        #siteinfo[request.user.username] = (stringresults,weather)

        ww.model = tf.keras.models.Sequential()
        tf.keras.backend.clear_session()
        return render(request, 'Combos/index.html', {
                'clothes': stringresults,
                'weatherinfo': weather
            })

#This function will add a good item to the NN
def trainnew(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":

        spec = request.POST.getlist('si')
        under = request.POST.getlist('fl')
        pant = request.POST.getlist('p')
        outer = request.POST.getlist('sl')
        coat = request.POST.getlist('wc')

        #All items are listed with one hot encoding
        good = [0,0,0,0,0,0,0,0,0,0,0,0,0]

        #The user will be brought back to the same page if they did not fill out an option
        if spec[0] == 'Choose...' or under[0] == 'Choose...' or pant[0] == 'Choose...' or outer[0] == 'Choose...' or coat[0] == 'Choose...':
            clothes = siteinfo[request.user.username][0]
            weather = siteinfo[request.user.username][1]

            return render(request, 'Combos/index.html', {
            'note':'Please select one option from each section',
            'clothes': clothes,
            'weatherinfo': weather
                })

        #A list is made and will contain all of the responses
        nums = []
        nums.append(int(spec[0]))
        nums.append(int(under[0]))
        nums.append(int(pant[0]))
        nums.append(int(outer[0]))
        nums.append(int(coat[0]))

        #Each num in nums contains the index of the clothing item they want to wear
        for num in nums:
            if num != -1:
                good[num] = 1.0

        #Weather info is retrieved and appended to clothing combo
        weatherinfo = ww.getweatherinfo(request)
        good = good + weatherinfo

        #1 is made for another list to represent a good combo
        result = [1]

        #The two lists are passed in as well as the request in order to retrain the NN
        ww.wt.retrain([good], [result], request)
        return HttpResponseRedirect(reverse("index"))

#This will render the how to use page for existing users if they are logged in
def howtouse(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'Combos/help.html')

#This will render the clothing help page if the user is logged in
def clothes(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'Combos/clothing.html')

#This will load the loading page before getting to the dashboard if the user is logged in.
def loading(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'Combos/loading.html')
