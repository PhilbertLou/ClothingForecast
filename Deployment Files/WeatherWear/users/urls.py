from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginpage, name="login"),
    path("logout", views.logoutpage, name="logout"),
    path("makeacc", views.makeacc, name="makeacc"),
    path("changeinfo", views.changeinfo, name="changeinfo"),
    path("changepass", views.changepass, name="changepass"),
    path("changeloc", views.changeloc, name="changeloc"),
    path("newuserhowtouse", views.newuserhowtouse, name="newuserhowtouse"),
    path("WeatherWear", views.WeatherWear, name="WeatherWear"),
    path("ClothingForecast", views.ClothingForecast, name="ClothingForecast"),
    path("<str:anything>", views.dirhome, name="dirhome"),
]
