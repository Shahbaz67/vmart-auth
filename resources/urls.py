from django.urls import path, include
from rest_framework import routers
from .auth import CreateTokenView
from .views import CustomUserViewSet, CompanyViewSet, LogoutView


router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'companies', CompanyViewSet, basename='companies')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', CreateTokenView.as_view(), name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
]