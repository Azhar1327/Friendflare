from django.contrib import admin
from .models import Profile, Post, Broadcast,LikePost, FollowersCount
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Broadcast)
admin.site.register(LikePost)
admin.site.register(FollowersCount)