"""
Model translations for core app
"""
from modeltranslation.translator import register, TranslationOptions
from .models import SliderItem, AboutSection, TeamMember, ContactInfo, ContactMessage, BlogPost, HomeInfoCard, HomeFeature


@register(SliderItem)
class SliderItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'button_text')


@register(AboutSection)
class AboutSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(TeamMember)
class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('name', 'position', 'bio')


@register(ContactInfo)
class ContactInfoTranslationOptions(TranslationOptions):
    fields = ('address',)


@register(BlogPost)
class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(HomeInfoCard)
class HomeInfoCardTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(HomeFeature)
class HomeFeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

