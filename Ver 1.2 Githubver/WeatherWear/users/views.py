from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import re, os
from . import NNdupe as nnd
from users.models import UserProfile
import requests, ast
from google.cloud import storage

dash = re.compile('[\'"-]')
key = 'WEATHERAPI KEY'
bucketname = 'BUCKET NAME'
storage_client = storage.Client.from_service_account_json('FILE PATH')

#This function will bring them to login page if they aren't logged in and if they are they will be brought to their dashboard/home page
def index(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return HttpResponseRedirect(f'http://philbert.pythonanywhere.com/Combos/{request.user.username}')

#This function deals with the log in page
def loginpage(request):
    if request.method == "POST":
        #Posted info is stored
        username = request.POST["username"]
        password = request.POST["password"]

        #DONT FORGET TO PREVENT SQL INJECTIONS
        #A user object will be returned if there is a user
        user = authenticate(request, username=username, password=password)

        #If there is a user they will be redirected to index
        if user is not None:
            login(request, user)

            #NEW
            bucket = storage_client.get_bucket(bucketname)
            blob = bucket.blob(f'{user.username}/{user.username}.data-00000-of-00001')
            blob.download_to_filename(f'/home/Philbert/Userdata/{user.username}/{user.username}.data-00000-of-00001')

            blob = bucket.blob(f'{user.username}/{user.username}.index')
            blob.download_to_filename(f'/home/Philbert/Userdata/{user.username}/{user.username}.index')

            return HttpResponseRedirect(reverse("index"))

        #If there is no user then they entered the wrong info and will be notified of that
        else:
            return render(request, "users/login.html", {
                "message":"Please enter right credentials"
            })

    #By default they will see the login html page
    return render(request, 'users/login.html')

#This function handles logging out the user
def logoutpage(request):

    #NEW
    bucket = storage_client.get_bucket(bucketname)
    blob = bucket.blob(f'{request.user.username}/{request.user.username}.data-00000-of-00001')
    blob.upload_from_filename(f'/home/Philbert/Userdata/{request.user.username}/{request.user.username}.data-00000-of-00001')
    os.remove(f'/home/Philbert/Userdata/{request.user.username}/{request.user.username}.data-00000-of-00001')

    blob = bucket.blob(f'{request.user.username}/{request.user.username}.index')
    blob.upload_from_filename(f'/home/Philbert/Userdata/{request.user.username}/{request.user.username}.index')
    os.remove(f'/home/Philbert/Userdata/{request.user.username}/{request.user.username}.index')

    logout(request)


    return render(request, "users/login.html", {
        "message": "Logged Out"
    })

#This function handles making user accounts
def makeacc(request):

    if request.method == "POST":
        #Posted info is saved
        username = request.POST["username"]
        password = request.POST["password"]
        city = request.POST["city"]
        country = request.POST["country"]

        #This gets the weather info for their proximity
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={key}&units=metric')
        content = response.content
        dictver = content.decode("UTF-8")
        weatherdata = ast.literal_eval(dictver)

        #This makes sure they do not have any special characters that would internally mess with the code
        if dash.search(username) != None or dash.search(password):
            return render(request, "users/makeacc.html", {
                "message":"Please do not include dash or quotations in your username or password."
            })
        #This makes sure that the username does not already exist
        elif User.objects.filter(username=username).exists():
            return render(request, "users/makeacc.html", {
                "message":"Please choose another username"
            })
        #This makes sure that the password is at least 8 characters long
        elif len(password) < 8:
            return render(request, "users/makeacc.html", {
                "message":"Please choose a password that is 8 characters or longer"
            })
        #This makes them re-enter their location if the location they entered is incorrect
        elif weatherdata['cod'] == '404':
            return render(request, "users/makeacc.html", {
                "message":"Please enter the correct city and country"
            })
        #Otherwise a user object can be created
        else:
            #User object, UserProfile, and the user's directory is saved
            user = User.objects.create_user(username=username, password=password)
            user.save()
            up = UserProfile(user=user, city=city, country=country)
            up.save()
            os.makedirs(f'/home/Philbert/Userdata/{user.username}')
            nnd.dupe(f'/home/Philbert/Userdata/{user.username}/{user.username}')


            #NEW
            bucket = storage_client.get_bucket(bucketname)
            blob = bucket.blob(f'{user.username}/{user.username}.data-00000-of-00001')
            blob.upload_from_filename(f'/home/Philbert/Userdata/{user.username}/{user.username}.data-00000-of-00001')
            os.remove(f'/home/Philbert/Userdata/{user.username}/{user.username}.data-00000-of-00001')

            blob = bucket.blob(f'{user.username}/{user.username}.index')
            blob.upload_from_filename(f'/home/Philbert/Userdata/{user.username}/{user.username}.index')
            os.remove(f'/home/Philbert/Userdata/{user.username}/{user.username}.index')

            return render(request, "users/login.html", {
                "message":"Account made. Please login."
            })
    return render(request, 'users/makeacc.html')

#This function deals with changing information
def changeinfo(request):
    return render(request, "users/changeinfo.html")

#This function deals with changing the password
def changepass(request):
    if request.method == "POST":
        #Saves posted values
        old = request.POST["oldpass"]
        new = request.POST["newpass"]

        #Authenticates the user first
        if authenticate(username=request.user.username, password=old):
            #Checks to see if the password is valid
            if dash.search(new):
                return render(request, "users/changeinfo.html", {
                    "message":"Please do not include dash or quotations in your password."
                })
            #Checks to see if the password is long enough
            elif len(new) < 8:
                return render(request, "users/changeinfo.html", {
                "message":"Please choose a password that is 8 characters or longer"
                })
            #If it passes all checks then the new password is created and user is brought to the login screen
            else:
                request.user.set_password(new)
                request.user.save()
                return render(request, "users/login.html", {
                    "message":"Password has been updated. Please sign in again"
                })

        #If user is not authenticated then they must enter their current password correctly this time and will be notified of that
        else:
            return render(request, "users/changeinfo.html", {
                "message":"Please enter right password"
            })

#This function handles changing the location of the user
def changeloc(request):
    if request.method == "POST":
        #Posted data is saved
        city = request.POST["city"]
        country = request.POST["country"]

        #Their new weather information is saved in a usable format
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={key}&units=metric')
        content = response.content
        dictver = content.decode("UTF-8")
        weatherdata = ast.literal_eval(dictver)

        #If the inputted location does not exist they will be notified of that
        if weatherdata['cod'] == '404':
            return render(request, "users/changeinfo.html", {
                "message":"Please enter a correct location. Use shortform for country (e.g. CA for Canada)"
            })

        #Otherwise their location will be updated in the UserProfile database
        else:
            entries = UserProfile.objects.filter(user=request.user)
            entry = entries.first()
            entry.city = city
            entry.country = country
            entry.save()
            return render(request, "users/changeinfo.html", {
                "message":"Location updated. Please check your dashboard to make sure that it is correct."
            })
    return render(request, 'users/changeinfo.html')
