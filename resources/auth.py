from .serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated


from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CreateTokenView(ObtainAuthToken):
    """
    Create a new auth token for existing user
    """
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id':user.id,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

 
class CustomizedUserPermission(IsAuthenticated):
    """
    Custom permission to list all users and to create any new user without authentication
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        if view.action == 'list':
            return True
        return super().has_permission(request, view)