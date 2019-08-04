
from django.http import HttpResponse
from django.shortcuts import render
from django import template
import logging
from django.utils.datastructures import MultiValueDictKeyError
from contacts.models import *
from django.db.models import Q

# Get an instance of a logger
logger = logging.getLogger(__name__)

def contacts_list(request , userparameter):
    users = Users.objects.all()
    conversations = Conversations.objects.all()
    messages = Messages.objects.filter(conversation_id = int(userparameter) )
    conv =  Conversations.objects.filter(id = userparameter)[0]
    convername = conv.name
    print('conversations:', conversations )

    if request.method == 'GET':

        # Received messages:1
        rezvan = Users.objects.filter(firstname='Rezvan')[0]
        Sent_messages = len(Messages.objects.filter(sender_id = rezvan))
        rezvanconv = rezvan.conversations_set.all()
        sum = 0
        for m in rezvanconv:
            sum += len(Messages.objects.filter(conversation_id = m))

        Received_messages = sum - Sent_messages 
        print('rezvan:', Received_messages )
        
        # 2
        queryset = 0
        for m in rezvanconv:
            queryset += len ( Messages.objects.filter(
                Q(conversation_id = m) & ~Q(sender_id = rezvan)
                ) 
            )
        print('rezvan:', queryset )

        # return HttpResponse( render(request,'chat.html'))

        return render(request,'chat.html', 
        {
            "conversations" : conversations ,
            "messages" : messages ,
            "convername" : convername
        }
            )

    elif request.method == 'POST' :
        print("request:" , request) 

        # new_conversation
        result = True
        try:
            for c in conversations:
                if request.POST['conversation-name'] in c.name:
                    result = False

            if  len(request.POST['conversation-name']) == 0 :
                logger.error("The name field can not be empty.")

            elif result == False:
                logger.error("This name is available in conversations")

            else:
                new_conversation = Conversations( name = request.POST['conversation-name'] , is_group = False ).save()
                
                
        except MultiValueDictKeyError:
            print("No conversation was add")
        
        # add_message
        try:
            print('add_message:', len(request.POST['add_message']) )
            if len(request.POST['add_message']) == 0:
                logger.error("No message was sent")
                print('no message')
            else:
                c = Conversations.objects.filter(id = int(userparameter))[0]
                Messages( sender_id = c.members.all()[0] , conversation_id = c , text = request.POST['add_message'] ).save()
                messages = Messages.objects.filter( conversation_id = int(userparameter))
                print(messages)
        except MultiValueDictKeyError:
            print(logger.error("No message was sent"))
    

        return render(request,'chat.html', 
        {
            "messages" : messages,
            "conversations" : conversations,
            "convername" : convername
        }
            )

# class Contact:
#     def __init__(self, classs , src , name , preview = " "):
#         self.classs = classs
#         self.src = src
#         self.name = name
#         self.preview = preview

#     def __str__(self):
#         return self.name

#     def get_fullname(self):
#         return "%s "  %(self.name)

# contacts=[ Contact("contact-status online" , "http://emilcarlsson.se/assets/louislitt.png" , "louis Litt" ,"You just got LITT up, Mike."),
#     Contact("contact-status busy" , "http://emilcarlsson.se/assets/harveyspecter.png" , "Harvey Specter", "Wrong. You take the gun, or you pull out a bigger one. Or, you call their bluff. Or, you do any one of a hundred and forty six other things."),
#     Contact("contact-status away" , "http://emilcarlsson.se/assets/rachelzane.png" , "Rachel Zane", "I was thinking that we could have chicken tonight, sounds good?"),
#     Contact("contact-status online" , "http://emilcarlsson.se/assets/donnapaulsen.png" , "Donna Paulsen" , "Mike, I know everything! I'm Donna.") ,
#     Contact("contact-status busy" , "http://emilcarlsson.se/assets/haroldgunderson.png" , "Harold Gunderson" , "Thanks Mike! ") ,
#     Contact("contact-status" ,  "http://emilcarlsson.se/assets/jessicapearson.png" , "Jessica Pearson" , "Have you finished the draft on the Hinsenburg deal?"),
#     Contact("contact-status busy" , "http://emilcarlsson.se/assets/katrinabennett.png", "Katrina Bennett" , "I've sent you the files for the Garrett trial."),
#     Contact("contact-status" , "http://emilcarlsson.se/assets/charlesforstman.png", "Charles Forstman" , "Mike, this isn't over."),
#     Contact("contact-status away" , "http://emilcarlsson.se/assets/jonathansidwell.png", "Jonathan Sidwell" , " That's bullshit. This deal is solid."),
#     ]

# Mike = Contact("contact-status online" , "http://emilcarlsson.se/assets/mikeross.png" , "Mike Ross" , " ")

# class Message:
#     def __init__(self, message_type, sender, receiver, message):
#         self.message_type = message_type 
#         self.sender = sender
#         self.receiver = receiver
#         self.message = message

#     def transfering_massage(self):
#         return self.sender.name +  'sent the message' +  self.message + "to" + self.receiver.name

# transfering = [ Message ( "sent" , contacts[0] , Mike ," How the hell am I supposed to get a jury to believe you when I am not even sure that I do?!"),
#                 Message ( "recive", Mike , contacts[0] , "When you're backed against the wall, break the god damn thing down."),
#                 Message ( "recive" , Mike , contacts[0] , "Excuses don't win championships."),
#                 Message ( "sent", contacts[0] , Mike  , "Excuses don't win championships."),
#                 Message ( "recive", Mike , contacts[0] , "No, I told him that."),
#                 Message ( "recive", Mike , contacts[0] , " What are your choices when someone puts a gun to your head?"),
#                 Message ( "sent" , contacts[0] , Mike  , "What are you talking about? You do what they say or they shoot you."),
#                 Message ( "recive" , Mike , contacts[0] , " Wrong. You take the gun, or you pull out a bigger one. Or, you call their bluff.")
# ]

# print (contacts)