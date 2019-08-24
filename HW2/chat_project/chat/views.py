
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse

from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist

from chat.models import Messages, Conversations
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from functools import wraps

from chat.serializer import ChatSerializer , Conversationserializer , ConversationListserializer , Return_all_messagesserializer,  Massageserializer ,  Editmessage
from chat_project.utiels import CsrfExemptSessionAuthentication
from rest_framework.authentication import BaseAuthentication

# # Response
class ConversationItem(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication , 
        BaseAuthentication )
    def post(self, request):
        serializer = Conversationserializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'massage':'Conversation saved successfuly'},
            status = status.HTTP_201_CREATED)
            
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST )
    def get(self , request):
        conversations = Conversations.objects.all()
        conv_serializer = ConversationListserializer(instance =conversations , many = True)
        return Response(conv_serializer.data,
            status = status.HTTP_200_OK)
            
# PythonDecorators/my_decorator.py

def my_decorator(view_func):
    def _decorator(request,*args,**kwargs):
        if request.user.is_anonymous():
            return Response({'message':'unauthorized'},
            statuse = status.HTTP_401_UNAUTHORIZED)
        else:
            view_func(request, *args, **kwargs) # Prove that function definition has completed
        return response
    return wraps(view_func)(_decorator)

@api_view(['POST'])
@my_decorator
def chatItem(request):

    serializer = ChatSerializer(data = request.POST, context = {'user': request.user}) 
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Message sent'} , status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,
            status = status.HTTP_400_BAD_REQUEST)

class ChatItem(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication , 
        BaseAuthentication )
    def post(self,request):
        print(request)
        print(request.COOKIES)
        print(request.user)

        if request.user.is_anonymous():
            return Response({'message':'unauthorized'}, statuse=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = ChatSerializer(data = request.POST, context = {'user': request.user}) 

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Message sent'} , status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors,
                    status = status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            instance = Messages.objects.get(id = request.data['message_id'])
            serializer = Editmessage (instance, data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(True)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST )
        except ObjectDoesNotExist:
           return Response({'message':'There is no message with this ID'}, status = status.HTTP_404_NOT_FOUND)

    def get(self, request):
        '''
        return all messages of conversation_id
        '''
        print(request.GET)
        serializer = Return_all_messagesserializer(data = request.GET)
        if serializer.is_valid():
            instance =  Messages.objects.filter(conversation_id = serializer.data['conversation_id'])
            massageserializer = Massageserializer(instance, many = True)
            return Response(massageserializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                status = status.HTTP_400_BAD_REQUEST)


# ********************** html
def conversation_view(request, userparameter):
    if request.method == 'GET':
        pass

    elif request.method == "POST":
        try:
            print(request.POST['message'])
            u = User.objects.filter(first_name="sara")[0]
            c = Conversations.objects.filter(
                id=int(userparameter))[0]
            Messages(
                sender_id=u,
                conversation_id=c,
                text=request.POST['message'],
                date=datetime.now()
            ).save()
        except ValueError:
            print("there is no userparameters")

    try:
        messages = Messages.objects.filter(conversation_id = int(userparameter))
    except ValueError:
        messages =  []

    return render(request,'conversationlist.html',
        {
            "messages": messages,"conversations": Conversations.objects.all()
        }
)   