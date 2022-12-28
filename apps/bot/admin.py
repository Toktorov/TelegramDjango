from django.contrib import admin
from apps.bot.models import User, UserPost

# Register your models here.
admin.site.register(User)
admin.site.register(UserPost)