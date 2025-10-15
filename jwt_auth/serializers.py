from rest_framework import serializers

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password  
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):   
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

  
    def validate(self, data):  
        print('RECEIVED DATA:', data)
        
        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')

       
        if password != password_confirmation:
            print('ERROR: Passwords do not match')
            raise serializers.ValidationError({'password_confirmation': 'Passwords do not match'})

        data['password'] = make_password(password)

        print('VALIDATED DATA:', data)
        return data

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'password_confirmation')
