from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import Review, Like, Comment
from .serializers import UserSerializer, ReviewSerializer, LikeSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.response import Response
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Welcome to the Movie Review API</h1>")
# Get the custom user model
User = get_user_model()

# Custom permission to check if the user is the owner of the review or comment
class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a review or comment to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# Pagination class for review results
class ReviewPagination(PageNumberPagination):
    page_size = 5  # Number of reviews per page
    page_size_query_param = 'page_size'
    max_page_size = 100

# ViewSet for User Management
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Allow any user to create an account, restrict others to authenticated users
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

# ViewSet for Review Management
class ReviewViewSet(viewsets.ModelViewSet):   
    """
    A viewset for viewing and editing review instances.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['movie_title']  # Allow searching by movie title
    ordering_fields = ['created_at', 'rating']  # Allow sorting by created date and rating
    ordering = ['-created_at']  # Default ordering (most recent first)

    # Define permissions by action
    permission_classes_by_action = {
        'update': [IsAuthenticated, IsOwner],
        'partial_update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],
    }

    def get_queryset(self):
        """
        Optionally restrict the returned reviews to a specific movie
        based on the `movie_title` query parameter.
        """
        queryset = super().get_queryset()
        movie_title = self.request.query_params.get('movie_title', None)
        if movie_title:
            queryset = queryset.filter(movie_title__icontains=movie_title)
        return queryset

    def get_permissions(self):
        """Return the correct permissions for each action."""
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super().get_permissions()

    def perform_create(self, serializer):
        """Attach the current logged-in user to the review."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='most-liked')
    def most_liked_reviews(self, request):
        """
        Get the top 5 most liked reviews for a movie.
        """
        movie_title = request.query_params.get('movie_title', None)
        if not movie_title:
            return Response({"detail": "Movie title is required."}, status=status.HTTP_400_BAD_REQUEST)

        most_liked = (Review.objects
                      .filter(movie_title__icontains=movie_title)
                      .annotate(likes_count=Count('like'))
                      .order_by('-likes_count')[:5])  # Get top 5 most liked reviews

        serializer = self.get_serializer(most_liked, many=True)
        return Response(serializer.data)

# ViewSet for Like Management
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create a like for a review, but prevent duplicate likes.
        """
        review_id = request.data.get('review')
        review = get_object_or_404(Review, id=review_id)  # Fetch review or return 404

        # Prevent duplicate likes
        if Like.objects.filter(user=request.user, review=review).exists():
            return Response({"detail": "You have already liked this review."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ViewSet for Comment Management
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Attach the current logged-in user to the comment.
        """
        serializer.save(user=self.request.user)
