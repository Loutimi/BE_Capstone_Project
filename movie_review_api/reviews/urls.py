from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ReviewViewSet, LikeViewSet, CommentViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'likes', LikeViewSet)  
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include((router.urls, 'api'), namespace='api')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


