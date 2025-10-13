from rest_framework.views import APIView # main API controller class
from rest_framework.response import Response #response class, like res object in express
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta # creates timestamps in dif formats
from django.contrib.auth import get_user_model # gets user model we are using
from django.conf import settings # import our settings for our secret
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
import jwt # import jwt

User = get_user_model() # Save user model to User var

class RegisterView(APIView):

    def post(self, request):
        print('REGISTRATION REQUEST DATA:', request.data)
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user = user_to_create.save()
            
            # Generate JWT token for the newly created user
            dt = datetime.now() + timedelta(days=7)
            token = jwt.encode(
                {'sub': str(user.id), 'exp': int(dt.strftime('%s'))},
                settings.SECRET_KEY,
                algorithm='HS256'
            )
            # Ensure token is returned as string
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            
            return Response({
                'token': token,
                'message': f'Welcome {user.username}!'
            }, status=status.HTTP_201_CREATED)
        print('SERIALIZER ERRORS:', user_to_create.errors)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):

    def post(self, request):
        print('LOGIN REQUEST DATA:', request.data)
        # get data from the request
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            print('ERROR: Missing username or password')
            raise PermissionDenied(detail='Please provide both username and password')
        
        try:
            user_to_login = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f'ERROR: User not found with username: {username}')
            raise PermissionDenied(detail='Invalid Credentials')
        
        if not user_to_login.check_password(password):
            print('ERROR: Invalid password')
            raise PermissionDenied(detail='Invalid Credentials')

        # timedelta can be used to calculate the difference between dates - passing 7 days gives you 7 days represented as a date that we can add to datetime.now() to get the date 7 days from now
        dt = datetime.now() + timedelta(days=7) # validity of token
        token = jwt.encode(
            {'sub': str(user_to_login.id), 'exp': int(dt.strftime('%s'))}, # strftime -> string from time and turning it into a number
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        # Ensure token is returned as string
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        print(f'SUCCESS: User {username} logged in')
        return Response({ 'token': token, 'message': f"Welcome back {user_to_login.username}"})

class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        serialized_user = UserSerializer(request.user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)
