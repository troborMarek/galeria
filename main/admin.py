from django.contrib import admin
from .models import User, Post, Rating


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'surname', 'email', 'bio']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user','title','image', 'description','price', 'apr_by_admin']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'score', 'date']
