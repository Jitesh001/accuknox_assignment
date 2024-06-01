from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FriendRequest, Friendship

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(FriendRequest)
admin.site.register(Friendship)

