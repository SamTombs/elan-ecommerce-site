from rest_framework import serializers
# function runs when creating superuser
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password  # hashes password for us
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()


# never converted to json and returned in response
class UserSerializer(serializers.ModelSerializer):
    # write_only=True ensures never sent back in JSON
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    # validate function is going to:
    # check our passwords match
    # hash our passwords
    # add back to database
    def validate(self, data):  # data comes from the request body
        print('RECEIVED DATA:', data)
        # remove fields from request body and save to vars
        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')

        # check if they match
        if password != password_confirmation:
            print('ERROR: Passwords do not match')
            raise serializers.ValidationError({'password_confirmation': 'Passwords do not match'})

        # checks if password is valid, comment this out so it works
        # TEMPORARILY DISABLED FOR DEVELOPMENT - RE-ENABLE FOR PRODUCTION!
        # try:
        #     password_validation.validate_password(password=password)
        # except DjangoValidationError as err:
        #     print('PASSWORD VALIDATION ERROR:', err.messages)
        #     raise serializers.ValidationError({'password': err.messages})

        # hash the password, reassigning value on dict
        data['password'] = make_password(password)

        print('VALIDATED DATA:', data)
        return data

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'password_confirmation')
