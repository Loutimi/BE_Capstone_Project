from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('User must have an email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255, null=True, blank=True, verbose_name='Email address')
    username = models.CharField(unique=True, max_length=150, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Require username for superuser creation

    def __str__(self):
        return self.username  # Display username as the string representation

def validate_rating(value):
    if not (1 <= value <= 5):
        raise ValidationError('Rating must be between 1 and 5.')
class Review(models.Model):
    movie_title = models.CharField(
        max_length=255, 
        blank=False,
        verbose_name="Movie Title"  # Add verbose_name for movie_title
    )
    content = models.TextField(blank=False)
    rating = models.PositiveIntegerField(
        validators=[validate_rating], 
        help_text='Please provide a rating between 1 and 5.',
        verbose_name="Movie Rating"  # Add verbose_name for rating
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')  # Prevent multiple likes by the same user on the same review

    def __str__(self):
        return f"{self.user.email} liked {self.review.movie_title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)  # Track when the comment was last modified

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.movie_title}"