
from django.db import models
from django.contrib.auth.models import User
import uuid

class Users(models.Model):
    username = models.CharField(max_length = 30)
    password = models.CharField( max_length = 50) 
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=10)
    birthday = models.DateField(null=True)
    number_of_friends = models.IntegerField()
    token = models.IntegerField(null=True)
    
    def __str__(self):
        return self.firstname + ' ' + self.lastname

class UserProfile(models.Model):
    #required by the auth model

    user = models.ForeignKey(User, on_delete = models.PROTECT , editable=True)
    token = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Verify_email(models.Model):
    
    user = models.ForeignKey(User, on_delete = models.PROTECT , editable=True)
    email_verified = models.BooleanField(null = False)
    verify_token = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
