from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('date_joined',)
    # Remove 'groups' and 'user_permissions' from filter_horizontal
    filter_horizontal = ()

    # Adjust list_filter to valid fields or attributes
    list_filter = ()
    
    fieldsets = ()


# Register your custom user model and admin class
admin.site.register(Account, AccountAdmin)
