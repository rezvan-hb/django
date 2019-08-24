
import datetime
from rest_framework import serializers
from chat.models import Messages , Conversations
from django.contrib.auth.models import User
from users1.models import UserProfile
from users1.serializer import ListUsers
from django.http import Http404

class ConversationListserializer(serializers.ModelSerializer):
    members = ListUsers(many=True, read_only=True)
    class Meta:
        model = Conversations
        fields = ['id' , 'name' , 'is_group' , 'members']


class Conversationserializer(serializers.Serializer):
    conversation_name = serializers.CharField(max_length = 100 , required= True )
    members = serializers.ListField( 
        child = serializers.IntegerField(min_value = 0 , max_value= 100) , allow_empty = True )
    is_group = serializers.BooleanField(default= False)

    def create(self, validate_data):
        c = Conversations( 
            name = validate_data['conversation_name'], 
            is_group = validate_data['is_group'] )

        c.save()
        userlist = User.objects.filter(id__in = validate_data['members'])
        print('userlist', userlist)
        for u in userlist:
            c.members.add(u)

        return c

class ChatSerializer(serializers.Serializer):
    # token = serializers.UUIDField()
    conversation_id = serializers.IntegerField(min_value = 1)
    text = serializers.CharField(max_length = 200)

    # def validate(self,data):
    #     try:
    #         self.user_profile = UserProfile.objects.get(token = data['token'])
    #     except objectDoesNotExist:
    #         # raise serializers.ValidationError('token is wrong!')
    #         raise  Http404('token is wrong!')
    #     return data

    def create(self ,validate_data):
        
        conversation = Conversations.objects.get( id = validate_data['conversation_id'] )
        m = Messages(
            # sender_id = self.user_profile.user ,
            sender_id = self.contex['user'],
            conversation_id = conversation ,
            text = validate_data['text'] ,
            date =  datetime.datetime.now())

        m.save()
        return m


class Editmessage(serializers.Serializer):
    message_id = serializers.IntegerField(min_value = 1)
    text = serializers.CharField(max_length = 200)

    def validate(self,data):
        try:
            message = Messages.objects.get(id = data['message_id'])
        except objectDoesNotExist:
            raise serializers.ValidationError('message id is wrong!')
        return data
    
    def update(self, instance, valid_data ):
        instance.text = valid_data.get('text', instance.text)
        instance.save()
        return instance

class Return_all_messagesserializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['conversation_id']
    
    def validate(self,data):
        try:
            massage = Messages.objects.get(conversation_id = data['conversation_id'])
        except objectDoesNotExist:
            raise serializers.ValidationError('There is not any conversation with this id!')
        return data

class  Massageserializer(serializers.ModelSerializer):
    conversation_id = ConversationListserializer()
    sender_id = ListUsers()
    class Meta:
        model = Messages
        fields = ['id','text','conversation_id','sender_id']
