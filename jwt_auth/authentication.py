from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings  # show secret key in settings.py
import jwt

User = get_user_model()


class JWTAuthentication(BasicAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        print('AUTH HEADER:', header)

        if not header:
            print('NO HEADER FOUND')
            return None

        if not header.startswith('Bearer'):
            print('HEADER DOES NOT START WITH BEARER')
            raise PermissionDenied(detail='Invalid Auth token')

        token = header.replace('Bearer ', '')
        print('TOKEN:', token[:50] + '...' if len(token) > 50 else token)

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            print('PAYLOAD:', payload)

            user = User.objects.get(pk=int(payload.get('sub')))
            print('USER FOUND:', user)

        except jwt.exceptions.InvalidTokenError as e:
            print('JWT ERROR:', str(e))
            raise PermissionDenied(detail='Invalid Token')

        except User.DoesNotExist:
            print('USER NOT FOUND')
            raise PermissionDenied(detail='User Not Found')

        return (user, token)
