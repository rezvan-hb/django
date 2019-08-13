
from rest_framework import serializers
from chat.models import Messages

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
