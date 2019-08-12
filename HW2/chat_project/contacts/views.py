
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
        # 3

        Received_messages = Messages.objects.filter(
            Q(conversation_id__in = Users.objects.filter(firstname='Rezvan')[0].conversations_set.all()) &
            ~Q(sender_id = Users.objects.filter(firstname='Rezvan')[0])).count()
        print('Rezvan:', Received_messages)

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


