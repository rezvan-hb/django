
from django.db import models

class Users(models.Model):

    username = models.CharField(max_length = 30)
    password = models.CharField( max_length = 50)
    
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=10)
    birthday = models.DateField(null=True)
    number_of_friends = models.IntegerField()

    def __str__(self):
        return self.firstname + ' ' + self.lastname