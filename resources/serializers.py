from rest_framework import serializers
from.models import CustomUser, Company
from django.contrib.auth import authenticate
from rest_framework import exceptions


class CompanySerializer(serializers.ModelSerializer):
    """
    Company serializer class
    """
    class Meta:
        model = Company
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Custom User serializer class
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    

class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    """
    Custom User serializer class only for retrieve action
    """
    class Meta:
        model = CustomUser
        exclude = ['is_active', 'is_staff', 'is_admin', 'groups', 'is_superuser', 'user_permissions']
        extra_kwargs = {'password': {'write_only': True}}


class AuthTokenSerializer(serializers.Serializer):
    """
    Auth token serializer class for validation email and password when logging in
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = ('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = ('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = ('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data
    