from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_moderator', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_moderator', 'is_active', 'groups')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('nickname', 'email', 'avatar')}),
        ('Права и роли', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_moderator', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 
                       'is_active', 'is_staff', 'is_superuser', 'is_moderator')}
        ),
    )
    
    search_fields = ('username', 'email', 'nickname')
    ordering = ('username',)
