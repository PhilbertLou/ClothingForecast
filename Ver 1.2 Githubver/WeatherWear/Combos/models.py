from django.db import models

# Create your models here.

class Person(models.Model):
    #link to users
    name = models.CharField(max_length=30)

    #this should store default file
    personalweight = "placeholder"

    #link to default weight

    def __str__(self):
        return self.name

#make this a many to many relation and prob add a section for this in each table
class DefaultWeight(models.Model):
    name = "Default"

    #put the place to store the default file next

    def __str__(self):
        return self.name
