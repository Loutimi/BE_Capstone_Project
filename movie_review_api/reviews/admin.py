from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as CustomUserAdmin
from .models import User, Review, Like, Comment

class UserAdmin(CustomUserAdmin):
    # Add custom fields to the admin display
    list_display = ['email', 'username', 'is_staff', 'is_active']
    ordering = ['email']
    search_fields = ['email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['movie_title', 'rating', 'user', 'created_at']
    search_fields = ['movie_title', 'user__username']
    ordering = ['-created_at']

class LikeAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'created_at']
    search_fields = ['review__movie_title', 'user__username']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'content', 'created_at']
    search_fields = ['review__movie_title', 'user__username', 'content']

# Register models to the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
