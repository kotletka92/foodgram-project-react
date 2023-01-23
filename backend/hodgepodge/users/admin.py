from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from users.models import Follow, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('pk',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    )
    list_filter = ('username', 'email')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'author',
                    )
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author')


admin.site.unregister(Group)
