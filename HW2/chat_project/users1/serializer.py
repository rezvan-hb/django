
from rest_framework import serializers
# from users1.models import Users
from django.contrib.auth.models import User
from users1.models import UserProfile
import uuid

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','first_name','last_name','email'] 
        extra_kwargs = {
            'email': {'allow_null': False ,'required': True }
            }
    
    def validate(self, data):
        if data['email'] == '' :
            raise serializers.ValidationError('Email field cannot be empty') 
        return data

    def create(self, validated_data):
        u = User(**validated_data)     
        u.set_password(validated_data['password'])
        u.save()
        return u

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required = True, allow_blank = False , max_length = 30)

    password = serializers.CharField(
        required = True, allow_blank=False , max_length = 50)
    
    

class EditProfile(serializers.Serializer):
    token = serializers.UUIDField(default=uuid.uuid4)
    class Meta:
        model = User
        fields = ['first_name','last_name','token']
    
    def validate(self , data):
        tokenlist = UserProfile.objects.values_list('token', flat=True)
        if data['token'] not in tokenlist:
            raise serializers.ValidationError('This token does not exist') 
        
        if 'first_name' not in data and 'last_name' not in data:
           raise serializers.ValidationError('??????')  
        return data

    def update(self, instance, data):
        print('validated_data:' , data)
        if 'first_name' in data:
            instance.first_name = data.get('first_name', instance.first_name)

        if 'last_name' in data:
            instance.last_name = data.get('first_name',instance.last_name)
        
        instance.save()
        return instance 


class ListUsers(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    def get_full_name(self,obj):
        return obj.first_name + ' ' + obj.last_name

    class Meta:
        model = User
        fields =['username','full_name','email'] 
  
        


    






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
