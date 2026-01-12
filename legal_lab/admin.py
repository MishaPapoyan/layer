"""
Customize Django Admin for multilingual support
"""
from django.contrib import admin

# Override admin site header
admin.site.site_header = "Legal Laboratory Admin"
admin.site.site_title = "Legal Laboratory Admin"
admin.site.index_title = "Welcome to Legal Laboratory Administration"

