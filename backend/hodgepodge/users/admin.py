from django.contrib.admin import ModelAdmin, register

from users.models import Follow, User


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('pk',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    )
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('pk',
                    'user',
                    'author',
                    )
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author')
