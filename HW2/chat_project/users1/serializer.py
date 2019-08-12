
from rest_framework import serializers
from users1.models import Users

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField( 
        required = True, allow_blank = False , max_length = 30
        )
    password = serializers.CharField( 
        required = True, allow_blank = False , max_length = 50
        )

class RequestGetSerializer(serializers.Serializer):
    firstname = serializers.CharField(required = False, allow_blank = False, max_length = 100)
    lastname = serializers.CharField(required = False, allow_blank = False, max_length = 100)

    def validate(self, data):
        if 'firstname' not in data and 'lastname' not in data:
            raise serializers.ValidationError(
                'At least one of firstname or lastname parameters are required'
            ) 
        return data


class UsersSerializer(serializers.Serializer):
    firstname = serializers.CharField(required=True, allow_blank=False, max_length=100)
    lastname = serializers.CharField(required=True, allow_blank=False, max_length=100)
    birthday = serializers.DateField()
    number_of_friends = serializers.IntegerField(default=10, min_value=0 )

    def  validate_number_of_friends(self, data):
        if data == 5: 
            raise serializers.ValidationError('you cant have 5 friends!' )
        return data      # return data

    # def validate (self, data):
    #     if data['number_of_friends'] > 5 and data['birthday'] == None
    #         raise serializers.ValidationError('!!!')
    #     return data
        
    def create(self, validated_data):
        print("I'm in the create function")
        u = Users( **validated_data )     # instance of Users in create function 
        u.save()
        return u
