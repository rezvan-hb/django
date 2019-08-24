
from django.contrib.auth.models import User 
from users1.models import UserProfile , Verify_email
from users1.serializer import UsersSerializer, RequestGetSerializer , LoginSerializer , SignupSerializer, EditProfile ,ListUsers 

from django.http import JsonResponse
from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from users1.models import Verify_email
from chat_project.utiels import CsrfExemptSessionAuthentication
from rest_framework.authentication import BaseAuthentication
from chat_project import celery
from users1.serializer import send_email
import uuid

class SignupItem(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication , 
        BaseAuthentication )
    
    def post(self, request):
        
        serializer = SignupSerializer(data = request.POST)

        if serializer.is_valid():
            verify_token = uuid.uuid4()
            user_save = serializer.save()     # User objects
            verify_email = Verify_email(
                user = user_save,
                email_verified = False, 
                verify_token = verify_token
            )
            verify_email.save()
            context = {'verify_token':verify_token}
            send_email(serializer.data,context)

            return Response({
                'message':'your account have been created successfuly!',
                "success": "Dear {} welcome.".format(user_save.username),
                'data':serializer.data
                }, status = status.HTTP_200_OK)

        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)  

class EmailVerification(APIView):
    def get(self, request, userparameter):
        print('userparam:', type(userparameter))
        uuid_parameter = uuid.UUID(userparameter)
        print('userparam:', type(uuid_parameter))
        
        instance = Verify_email.objects.filter(verify_token = userparameter)[0]
        instance.email_verified = True
        instance.save()
        print(instance)

        return Response(
            {
            'message':'your account have been verified successfuly!',
            }, 
            status = status.HTTP_200_OK
        )


class LoginItem(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication ,BaseAuthentication )

    def post(self, request):
        serilizer = LoginSerializer(data = request.POST)
        if serilizer.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username = username, password = password)
            
            print('user:', user)
            if user is not None:
                if user.is_active:
                    if Verify_email.objects.get(user = user).email_verified :
                        login(request, user)
                
                        return Response({
                                'message': 'Your email has not been verified'
                                }, status = status.HTTP_403_FORBIDDEN)
                    else:
                        return Response({
                                'message': 'You have successfully logged in.'
                                }, status = status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    'message': 'There is not any account with this username/password!' 
                },status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serilizer.errors , status = status.HTTP_400_BAD_REQUEST)

class EditProfileItem(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication , 
        BaseAuthentication )
    def put(self, request):
        '''
        edit profile
        '''
        userp = request.user
        serializer = EditProfile( 
            instance = userp , data = request.data)

        if serializer.is_valid():
            print('serializer.data:', serializer.validated_data)
            serializer.save()
            return  Response({'message':'edit profile successfully!'}, status = status.HTTP_200_OK)
        else:
            return  Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        '''
            get users list:
        '''
        Userp = User.objects.all()
        serializer = ListUsers(instance = Userp , many = True)
        return  Response({'data': serializer.data },
            status = status.HTTP_200_OK)

# /////////////////////////////////////////////////////////////////////////////////////
 
class ListUsersItem(APIView):
    def get(self, request):
        """
        Return a list of all users.
        """
        request_serializer = RequestGetSerializer( data = request.GET)

        if request_serializer.is_valid():
            users = User.objects
            if 'firstname' in request_serializer.data:
                users = users.filter(firstname = request_serializer.data['firstname'])

            if 'lastname' in request_serializer.data:
                users = users.filter(lastname = request_serializer.data['lastname'])

            response_serializer = UsersSerializer( instance = users , many = True) 
            print(response_serializer)   
            return  Response({
                'data': response_serializer.data
                }, status = status.HTTP_200_OK)  # querydict type

        else:
            return  Response(
                request_serializer.errors,
                status = status.HTTP_400_BAD_REQUEST        
            )

    def post(self, request):
        """
        """
        print('data:', request.POST )
        serializer = UsersSerializer( data = request.POST)

        if serializer.is_valid():
            serializer.save()    # create function   
        else:
            return Response( serializer.errors , status = status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data } , status = status.HTTP_201_CREATED )

    def delete(self, request):
        return Response({ 'data': 'delete function' })

    def put(self, request):
        return Response({ 'data': 'put function' })


@csrf_exempt
def users_list_item(request):
    if request.method == 'GET':
        request_serializer = RequestGetSerializer( data = request.GET)
        print(request.GET)
        print(request_serializer)
        if request_serializer.is_valid():
            users = User.objects
            if 'firstname' in request_serializer.data:
                users = users.filter(firstname = request_serializer.data['firstname'])

            if 'lastname' in request_serializer.data:
                users = users.filter(lastname=request_serializer.data['lastname'])

            response_serializer = UsersSerializer( instance = users , many = True)    
            return JsonResponse({ 'data': response_serializer.data })  # querydict type

        else:
            return JsonResponse(
                request_serializer.errors,
                status = 400
            )

    elif request.method == 'POST':
        print('data:', request.POST )
        serializer = UsersSerializer(data = request.POST)

        if serializer.is_valid():
            serializer.save()    # create function   
        else:
            return JsonResponse( serializer.errors , status = 400 )

        return JsonResponse({'data': serializer.data })


# ******************************************************************************************

# def user_list_item(request):
#     if request.method == 'GET':
#         user_list = []
#         users = User.objects

#         if 'firstname' in request.GET:
#             users = users.filter(firstname = request.GET['firstname'])
        
#         if 'lastname' in request.GET:
#             users = users.filter( lastname = request.GET['lastname'])
         
#         if 'firstname' not in request.GET and 'lastname' not in request.GET:
#             users = []

#         for u in users:
#            user_list.append({
#                 'firstname' : u.firstname,
#                 'lastname' : u.lastname,
#                 'id' : u.id
#                }) 

#         return Jsonresponse({
#             'data' : user_list
#             })

#     elif request.method =='POST':
#         firstname = request.POST['firstname']
#         lastname = request.POST['lastname']
#         number_of_friends = request.POST['number_of_friends']
#         birthday = datetime.fromisoformat(request.POST['birthday'])    # iso 8601 Date and time: 2019-08-09T08:12:10+00:00

#         try:
#             number_of_friends = int(number_of_friends)
#         except ValueError:
#             return Jsonresponse({
#                 'Message' : 'number of friends must be an integer field'
#             }, status = 400 )

#         if len(firstname) and len(lastname) > 100:
#             return Jsonresponse({
#                 'Message' : 'first/last name  must be less than 100 chars'
#             }, status = 400 )

#         parsed_birthday = dp.parse(birthday)
#         year_birthday=parsed_birthday.year

#         if ( 2019 - year_birthday ) < 15:
#             return Jsonresponse({
#                 'Message' : 'Age under 15 is not allowed'
#             }, status = 400 )

#         u = User(
#             firstname = firstname,
#             lastname = lastname,
#             birthday = birthday,
#             number_of_friends = number_of_friends
#         )
#         u.save()

#         return Jsonresponse({
#             'data': {
#                 'firstname' = u.firstname,
#                 'lastname' = u.lastname,
#                 'birthday' = u.birthday,
#                 'friends' = u.number_of_friends,
#                 'id' = u.id
#             }
#         })
