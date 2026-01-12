# Multilingual Setup - Legal Laboratory

The application now supports three languages:
- 🇬🇧 **English** (en)
- 🇦🇲 **Armenian** (hy)
- 🇷🇺 **Russian** (ru)

## Features

### 1. Language Switcher
- Located in the navigation menu with flag icons
- Hover dropdown to select language
- Current language is highlighted
- Language selection persists across pages

### 2. Admin Panel Multilingual Support
All content can be added in three languages through the Django Admin Panel:

**Core App:**
- Slider Items (title, description, button_text)
- About Sections (title, content)
- Team Members (name, position, bio)
- Contact Info (address)

**Education App:**
- Categories (name, description)
- Articles (title, content, excerpt, author)
- Exam Materials (title, description)

**Games App:**
- Game Types (name, description)
- Games (title, description, scenario)
- Questions (question_text)
- Answers (answer_text, explanation)

**Cases App:**
- Legal Cases (title, description, scenario, evidence)

**News App:**
- Categories (name, description)
- Articles (title, content, excerpt, author)

### 3. How to Add Multilingual Content in Admin

1. **Login to Admin Panel**: http://127.0.0.1:8000/admin/
2. **Navigate to any model** (e.g., Slider Items, Articles, etc.)
3. **You'll see tabs for each language**: English, Հայերեն (Armenian), Русский (Russian)
4. **Fill in content for each language** you want to support
5. **Save** - the content will automatically display in the user's selected language

### 4. User Language Selection

Users can change language using:
- **Navigation Menu**: Click the flag dropdown in the top navigation
- **Language persists**: Selected language is saved in session
- **Automatic fallback**: If content is not available in selected language, it falls back to English

## Technical Details

### Packages Used
- `django-modeltranslation`: Handles multilingual database fields
- Django's built-in `i18n` framework: Handles URL routing and language selection

### Database Structure
Each translatable field has three versions:
- `field_name` (original, uses default language)
- `field_name_en` (English)
- `field_name_hy` (Armenian)
- `field_name_ru` (Russian)

### URL Structure
- Default (no language prefix): Uses default language (English)
- `/en/...`: English
- `/hy/...`: Armenian
- `/ru/...`: Russian

## Adding New Translatable Content

To add translations to a new model:

1. Create a `translation.py` file in your app
2. Register the model with `@register(ModelName)`
3. Define translatable fields in `TranslationOptions`
4. Update admin to use `TranslationAdmin`
5. Run migrations: `python manage.py makemigrations && python manage.py migrate`

Example:
```python
from modeltranslation.translator import register, TranslationOptions
from .models import YourModel

@register(YourModel)
class YourModelTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content')
```

## Notes

- Content in admin shows separate fields for each language
- If a field is empty in a language, it will fallback to the default (English)
- All template strings should use `{% trans "..." %}` for translation
- Static strings in templates are translated using Django's translation framework

