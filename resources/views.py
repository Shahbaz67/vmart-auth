from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import Company, CustomUser
from .serializers import CompanySerializer, CustomUserSerializer, CustomUserRetrieveSerializer
from .backends import EmailTokenAuthentication
from .auth import CustomizedUserPermission


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Company Modelviewset
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Custom user ModelViewset
    """
    queryset = get_user_model().objects.all()
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
    """
    Logout view that deletes the authenticated user token
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

