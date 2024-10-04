from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ReviewViewSet, LikeViewSet, CommentViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create a schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Movie Review API",
        default_version='v1',
        description="API documentation for the Movie Review application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@moviereview.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Set up the router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'likes', LikeViewSet)  
router.register(r'comments', CommentViewSet)

# Define URL patterns
urlpatterns = [
    path('', include((router.urls, 'api'), namespace='api')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger and ReDoc URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


