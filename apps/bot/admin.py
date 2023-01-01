from django.contrib import admin
from apps.bot.models import User, UserPost

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', )
    list_display = ('username', 'id_telegram', 'first_name', 'last_name', 'chat_id', 'date_joined')
    search_fields = ('username', 'id_telegram', 'first_name', 'last_name', 'chat_id', 'date_joined')
    list_per_page = 20

class UserPostAdmin(admin.ModelAdmin):
    list_filter = ('title', )
    list_display = ('title', 'description', 'created')
    search_fields = ('title', 'description', 'created')
    list_per_page = 30

admin.site.register(User, UserAdmin)
admin.site.register(UserPost, UserPostAdmin)