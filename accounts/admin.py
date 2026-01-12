from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'account_type', 'total_points', 'is_staff', 'date_joined']
    list_filter = ['account_type', 'is_staff', 'is_superuser']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('account_type', 'profile_image', 'phone', 'bio', 'total_points')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('account_type', 'email')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'saved_cases_count', 'saved_articles_count']
    filter_horizontal = ['saved_cases', 'saved_articles']
    
    def saved_cases_count(self, obj):
        return obj.saved_cases.count()
    saved_cases_count.short_description = 'Saved Cases'
    
    def saved_articles_count(self, obj):
        return obj.saved_articles.count()
    saved_articles_count.short_description = 'Saved Articles'

