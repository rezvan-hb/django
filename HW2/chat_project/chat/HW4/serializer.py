from rest_framework import serializers
from chat.models import Messages , Conversations
from users1.models import Users

class NumberofMessage(serializers.Serializer):
    conversation_id = serializers.IntegerField(min_value = 1 ,required = True)
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    size = serializers.IntegerField(default = 5)

    def validate(self, data):
        if data['from_date'] > data['to_date']:
            raise serializers.ValidationError("finish must occur after start")
        return data

class Messageserializer(serializers.ModelSerializer):
    conversation_id = serializers.IntegerField(min_value = 1,required = True)
    sender_id = serializers.IntegerField(min_value = 1,required = True)
    message = serializers.CharField()

    def validate(self, data):
        c = Conversations.objects.get(id = data['conversation_id'])
        u = Users.objects.get(id = data['sender_id'])
        
        if u not in c.members:
            raise serializers.ValidationError(
                '.........'
            )
        return data

    def create(self ,validate_data):
        user = Users.objects.get(id = validate_data['sender_id'])
        conversation = Conversations.objects.get(id = validate_data['conversation_id'])
        m = Messages(
            sender_id = user ,
            conversation_id = conversation,
            text = validate_data['text'],
            date = '2019-02-05',
        )
        m.save()
        return m
