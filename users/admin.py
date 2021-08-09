from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_subscribed', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Subscription', {'fields': ('last_subscription', 'duration_subscription')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'first_name', 'last_name', 'last_subscription',
                'duration_subscription'),
        }),
    )
