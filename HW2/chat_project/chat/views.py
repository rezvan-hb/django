
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

from users1.models import Users
from chat.models import Messages, Conversations

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chat.serializer import ChatSerializer

class ChatItem(APIView):
    def post(self, request):
        serializer = ChatSerializer(data = request.POST )
        if serializer.is_valid():
            u= serializer.save()
            return Response(
                {
                    'firstname' : u.sender_id.firstname ,
                    'date' : u.date ,
                    'text' : u.text
                }
            )
        return Response(
            serializer.errors
        )


def conversation_view(request, userparameter):
    if request.method == 'GET':
        pass

    elif request.method == "POST":
        try:
            print(request.POST['message'])
            u = Users.objects.filter(first_name="sara")[0]
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
        messages = Messages.objects.filter(
            conversation_id=int(userparameter)
        )
    except ValueError:
        messages =  []

    return render(
        request,
        'conversationlist.html',
        {
            "messages": messages,
            "conversations": Conversations.objects.all()
        }
)