from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#This model links together a user, a city, and a country
class UserProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   city = models.CharField(max_length=64)
   country = models.CharField(max_length=64)

   def __str__(self):
        return self.user.username