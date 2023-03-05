from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')

class StylesAdmin(admin.ModelAdmin):
    list_display = ('id', 'style_name')
    list_display_links = ('id', 'style_name')
    search_fields = ('style_name',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Styles, StylesAdmin)
