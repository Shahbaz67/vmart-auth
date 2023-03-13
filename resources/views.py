from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import Company, CustomUser
from .serializers import CompanySerializer, CustomUserSerializer, AuthTokenSerializer, CustomUserRetrieveSerializer
from .backends import EmailTokenAuthentication
from .auth import CustomizedUserPermission


User = get_user_model()

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]

    # def get_queryset(self):
    #     return Company.objects.filter(user=self.request.user)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [EmailTokenAuthentication]
    permission_classes = [CustomizedUserPermission]

    def get_serializer_class(self):
        if self.action=='retrieve':
            return CustomUserRetrieveSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get("email")
        password = request.data.get('password')
        if not email or not password:
            return Response({"Email and password must be provided"})  
        if serializer.is_valid():
            user = serializer.save()
            user.password = make_password(user.password)
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

