from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import SliderItem, AboutSection, TeamMember, ContactInfo, ContactMessage, BlogPost, Partner, HomeInfoCard, HomeFeature


@admin.register(SliderItem)
class SliderItemAdmin(TranslationAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']


@admin.register(AboutSection)
class AboutSectionAdmin(TranslationAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin):
    list_display = ['name', 'position', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(ContactInfo)
class ContactInfoAdmin(TranslationAdmin):
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    search_fields = ['name', 'email', 'subject', 'message']


@admin.register(BlogPost)
class BlogPostAdmin(TranslationAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']


@admin.register(HomeInfoCard)
class HomeInfoCardAdmin(TranslationAdmin):
    list_display = ['title', 'icon', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']


@admin.register(HomeFeature)
class HomeFeatureAdmin(TranslationAdmin):
    list_display = ['title', 'icon', 'highlight_number', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']

