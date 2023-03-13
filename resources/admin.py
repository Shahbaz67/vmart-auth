from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company


class CustomUserAdmin(UserAdmin):
    """
    Custom user admin for CustomUser model
    """
    fieldsets = (
        (None, {'fields': ('email', 'password', 'company', 'first_name', 'last_name', 'age', 'bio', 'gender')}),
        ('Permissions', {'fields': ('is_admin', 'is_active','is_superuser',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email','password1', 'password2',)
            }
        ),
    )

    list_display = ('email',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()  


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Company)