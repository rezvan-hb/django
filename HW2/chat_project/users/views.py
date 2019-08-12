
from django.http import HttpResponse
from django.shortcuts import render
from django import template
# import the logging library
import logging
from django.utils.datastructures import MultiValueDictKeyError


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Contact:
    def __init__(self, classs , src , name , preview = " "):
        self.classs = classs
        self.src = src
        self.name = name
        self.preview = preview

    def __str__(self):
        return self.name

    def get_fullname(self):
        return "%s "  %(self.name)

contacts=[ Contact("contact-status online" , "http://emilcarlsson.se/assets/louislitt.png" , "louis Litt" ,"You just got LITT up, Mike."),
    Contact("contact-status busy" , "http://emilcarlsson.se/assets/harveyspecter.png" , "Harvey Specter", "Wrong. You take the gun, or you pull out a bigger one. Or, you call their bluff. Or, you do any one of a hundred and forty six other things."),
    Contact("contact-status away" , "http://emilcarlsson.se/assets/rachelzane.png" , "Rachel Zane", "I was thinking that we could have chicken tonight, sounds good?"),
    Contact("contact-status online" , "http://emilcarlsson.se/assets/donnapaulsen.png" , "Donna Paulsen" , "Mike, I know everything! I'm Donna.") ,
    Contact("contact-status busy" , "http://emilcarlsson.se/assets/haroldgunderson.png" , "Harold Gunderson" , "Thanks Mike! ") ,
    Contact("contact-status" ,  "http://emilcarlsson.se/assets/jessicapearson.png" , "Jessica Pearson" , "Have you finished the draft on the Hinsenburg deal?"),
    Contact("contact-status busy" , "http://emilcarlsson.se/assets/katrinabennett.png", "Katrina Bennett" , "I've sent you the files for the Garrett trial."),
    Contact("contact-status" , "http://emilcarlsson.se/assets/charlesforstman.png", "Charles Forstman" , "Mike, this isn't over."),
    Contact("contact-status away" , "http://emilcarlsson.se/assets/jonathansidwell.png", "Jonathan Sidwell" , " That's bullshit. This deal is solid."),
    ]

Mike = Contact("contact-status online" , "http://emilcarlsson.se/assets/mikeross.png" , "Mike Ross" , " ")

class Message:
    def __init__(self, message_type, sender, receiver, message):
        self.message_type = message_type 
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def transfering_massage(self):
        return self.sender.name +  'sent the message' +  self.message + "to" + self.receiver.name

transfering = [ Message ( "sent" , contacts[0] , Mike ," How the hell am I supposed to get a jury to believe you when I am not even sure that I do?!"),
                Message ( "recive", Mike , contacts[0] , "When you're backed against the wall, break the god damn thing down."),
                Message ( "recive" , Mike , contacts[0] , "Excuses don't win championships."),
                Message ( "sent", contacts[0] , Mike  , "Excuses don't win championships."),
                Message ( "recive", Mike , contacts[0] , "No, I told him that."),
                Message ( "recive", Mike , contacts[0] , " What are your choices when someone puts a gun to your head?"),
                Message ( "sent" , contacts[0] , Mike  , "What are you talking about? You do what they say or they shoot you."),
                Message ( "recive" , Mike , contacts[0] , " Wrong. You take the gun, or you pull out a bigger one. Or, you call their bluff.")
]

print (contacts)

def user_list(request):
    
    if request.method == 'GET':
    # return HttpResponse( render(request,'chat.html') )
        return render(request,'chathtml.html', 
        {
            "contacts" :contacts,
            "transfering" :transfering
        }
                    )
    elif request.method == 'POST' :
        print("request:" , request) 

        # new_contact
        result = True
        try:
            for c in contacts:
                if request.POST['contact-name'] in c.name:
                    result = False

            if  len(request.POST['contact-name']) == 0 :
                logger.error("The name field can not be empty.")

            elif result == False:
                logger.error("This name is available in contacts")

            else:
                new_contact = Contact("contact-status","https://www.kasandbox.org/programming-images/creatures/Hopper-Cool.png" , request.POST['contact-name'] , " ")
                contacts.append(new_contact)
        except MultiValueDictKeyError:
            print("No contact was add")
        
        # add_message
        try:
            print('add_message:', len(request.POST['add_message']) )
            if len(request.POST['add_message']) == 0:
                logger.error("No message was sent")
                print('no message')
            else:
                add_transfering = Message( "recive" , Mike , contacts[0] , request.POST['add_message'])
                transfering.append(add_transfering)  
                print(len(transfering))
                print(add_transfering.message)
        except MultiValueDictKeyError:
            print(logger.error("No message was sent"))

        return render(request,'chat.html', 
        {
            "contacts":contacts,
            "transfering" :transfering,
            "transfering_count": len(transfering)
        }
            )