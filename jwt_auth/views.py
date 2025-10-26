from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
import jwt

User = get_user_model()

class RegisterView(APIView):

    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user = user_to_create.save()
            
            dt = datetime.now() + timedelta(days=7)
            token = jwt.encode(
                {'sub': str(user.id), 'exp': int(dt.strftime('%s'))},
                settings.SECRET_KEY,
                algorithm='HS256'
            )
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            
            return Response({
                'token': token,
                'message': f'Welcome {user.username}!'
            }, status=status.HTTP_201_CREATED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            raise PermissionDenied(detail='Please provide both username and password')
        
        try:
            user_to_login = User.objects.get(username=username)
        except User.DoesNotExist:
            raise PermissionDenied(detail='Invalid Credentials')
        
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail='Invalid Credentials')

        dt = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {'sub': str(user_to_login.id), 'exp': int(dt.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        return Response({ 'token': token, 'message': f"Welcome back {user_to_login.username}"})

class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        serialized_user = UserSerializer(request.user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)
