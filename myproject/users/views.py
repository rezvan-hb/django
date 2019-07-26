
from django.http import HttpResponse
from django.shortcuts import render
from django import template
# from django.template import loader
from django.template import engines

class User:
    def __init__(self,firstname,lastname,grades=[]):
        self.firstname = firstname
        self.lastname = lastname
        self.grades = grades

    def __str__(self):
        return self.firstname + ' ' + self.lastname

    def get_fullname(self):
        return "%s %s"  %(self.firstname , self.lastname)

users=[
    User('Rezvan','Habibi',[1, 2, 5]),
    User('Ali','Alavi',[ 5, 8, 10]),
    User('Sara','Ahmadi',[10 , 11 ,5]),
]    

# Create your views here.

def user_list(request):
    # c = {'foo': 'bar'}
    # t = loader.get_template('index.html')
    # return HttpResponse(t.render(c , request))
     return HttpResponse( render(request,'indexfile.html') )

# def user_list(request):
#     """
#     Rezvan Habibi
#     <br />
#     Ali Alavi
#     <br />
#     Sara Ahmadi
#     """
#     text=""
#     for u in users:
#         text += "<br />"
#         text += u.get_fullname()
#     return HttpResponse( "<html> This is the list of users: %s<html/>"  %text)
