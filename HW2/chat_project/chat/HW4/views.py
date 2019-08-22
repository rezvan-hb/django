
from datetime import datetime , date

from users1.models import Users
from chat.models import Messages, Conversations

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chat.HW4.serializer import NumberofMessage, Messageserializer

# HW4:
class MessageView(APIView):
    def get(self,request):
        serializer_NOM= NumberofMessage(data =request.GET)
        print( 'nbkjdnbkl:', serializer_NOM.data['from_date'] , type(serializer_NOM.data['from_date']) )

        if serializer_NOM.is_valid():
            if 'to_date' not in serializer_NOM.data or 'from_date' not in serializer_NOM.data:
                messagelist = Messages.objects.all()
            else:
                messages = Messages.objects.filter(conversation_id = serializer_NOM.data['conversation_id'])
                NOM=0
                messagelist=[]
                print(messages)
        
                for m in messages:
                    # if int(m.date.datetime.strftime('%Y%m%d')) >= int(serializer_NOM.data['from_date'].datetime.strftime('%Y%m%d'))  and   int(m.date.datetime.strftime('%Y%m%d')) <= int(serializer_NOM.data['to_date'].datetime.strftime('%Y%m%d')):
                    if m.date > serializer_NOM.data['from_date']:
                        NOM +=1 
                        messagelist.append(m)
                
                if NOM >  serializer_NOM.data['size']:
                    return Response({
                        'message':'number of message is more than size!'
                    })

            messageserializer = Messageserializer(instance = messagelist , many = True)
            return Response({
                'converasation_id':serializer_NOM.data['conversation_id'] ,
                'Number of Message' : NOM ,
                'data': messageserializer.data
                })
        else:
            return Response(serializer_NOM.errors)

    def post(self,request):
        messageserializer = Messageserializer( data=request.POST )
        if messageserializer.is_valid():
            messageserializer.save()
            return Response({
                'message':'Message saved'})
        else:
            return Response( messageserializer.errors )
# # # # # 