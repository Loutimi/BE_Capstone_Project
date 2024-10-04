from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Review, Like, Comment
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


# Get the custom user model
User = get_user_model()

# Serializer for the User Model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']  
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False},
            'username': {'required': True, 'allow_blank': False},
        }

    def create(self, validated_data):
        # Create a user with a hashed password
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Allow password update
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_password(self, value):
        """Validate the password against Django's password validation rules."""
        validate_password(value)  # Call Django's password validation
        return value

# Serializer for the Review Model
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Shows the reviewer's username

    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'content', 'rating', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']  # These fields shouldn't be edited

    def validate_rating(self, value):
        """Ensure the rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise ValidationError('Rating must be between 1 and 5')
        return value

    def validate(self, attrs):
        """Ensure required fields are provided."""
        if not attrs.get('movie_title'):
            raise ValidationError('Movie title is required.')
        if not attrs.get('content'):
            raise ValidationError('Review content is required.')
        return attrs

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'review']
        read_only_fields = ['user']

# Serializer for the Comment Model
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Shows the commenter's username

    class Meta:
        model = Comment
        fields = ['id', 'user', 'review', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']