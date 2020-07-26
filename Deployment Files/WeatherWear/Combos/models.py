from django.db import models

# Create your models here.

#Old class, could be implemented in the future

class Person(models.Model):
    #link to users
    name = models.CharField(max_length=30)

    #this should store default file
    personalweight = "placeholder"

    #link to default weight

    def __str__(self):
        return self.name

class DefaultWeight(models.Model):
    name = "Default"

    def __str__(self):
        return self.name
