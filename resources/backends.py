from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailBackend(BaseBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None 
        else:
            if user.password==password:
                return user
        return None


class EmailTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        UserModel = get_user_model()
        try:
            token = self.get_model().objects.get(key=key)
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        # Authenticate using the custom backend that checks for email/password
        user = EmailBackend().authenticate(email=token.user.email, password=token.user.password)

        if not user:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (user, token)
