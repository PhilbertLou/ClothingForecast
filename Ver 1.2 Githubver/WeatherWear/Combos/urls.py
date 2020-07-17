from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("remove", views.remove, name="remove"),
    path("getbackup", views.getbackup, name="getbackup"),
    path("trainnew", views.trainnew, name="trainnew"),
    path("<str:username>", views.index, name="usercombo"),
]
