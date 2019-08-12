
from datetime import datetime
import dateutil.parser as dp

from users1.models import Users
from users1.serializer import UsersSerializer, RequestGetSerializer , LoginSerializer , SignupSerializer

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

class SignupItem(APIView):
    def post(self, request):
        serializer = SignupSerializer(data = request.POST )
        if serializer.is_valid():
            r
        return Response(
            serializer.errors)    


class LoginItem(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.POST )
        if serializer.is_valid() :
            try:
                u = Users.objects.get( username = request.POST['username'] )
                if request.POST['password'] == u.password:  
                    return  Response({
                        'message': 'Your accound info is correct!' , 
                        'data': {
                            'firstname' : u.firstname
                            }
                        },
                        status = status.HTTP_200_OK)
                else:
                    return  Response({
                        'message': 'Your password is wrong!' 
                        },
                        status = status.HTTP_404_NOT_FOUND)

            except ObjectDoesNotExist:
                return  Response({
                    'message': 'There is not any account with this username!' 
                }, status = status.HTTP_404_NOT_FOUND)
        
        else:
            return  Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST)

class ListUsersItem(APIView):
    def get(self, request):
        """
        Return a list of all users.
        """
        request_serializer = RequestGetSerializer( data = request.GET)

        if request_serializer.is_valid():
            users = Users.objects
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
            users = Users.objects
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
        
# def user_list_item(request):
#     if request.method == 'GET'
#         user_list = []
#         users = Users.objects

#         if 'firstname' in request.GET:
#             users = users.filter(firstname = request.GET['firstname'])
        
#         if 'lastname' in request.GET:
#             users = users.filter( lastname = request.GET['lastname'])
         
#         if 'firstname' not in request.GET and 'lastname' not in request.GET:
#             users = []

#         for u in users:
#            user_list.append({
#                 'firstname' : u.firstname
#                 'lastname' : u.lastname
#                 'id' : u.id
#                }) 

#         return Jsonresponse({
#             'data' : user_list
#             })

#     elif request.method = 'POST':
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

#         if len(firstname) and len(lastname) > 100
#             return Jsonresponse({
#                 'Message' : 'first/last name  must be less than 100 chars'
#             }, status = 400 )

#         parsed_birthday = dp.parse(birthday)
#         year_birthday=parsed_birthday.year

#         if ( 2019 - year_birthday ) < 15
#             return Jsonresponse({
#                 'Message' : 'Age under 15 is not allowed'
#             }, status = 400 )

#         u = Users(
#             firstname = firstname
#             lastname = lastname
#             birthday = birthday
#             number_of_friends = number_of_friends
#         )
#         u.save()

#         return Jsonresponse({
#             'data': {
#                 'firstname' = u.firstname
#                 'lastname' = u.lastname
#                 'birthday' = u.birthday
#                 'friends' = u.number_of_friends
#                 'id' = u.id
#             }
#         })
