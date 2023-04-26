from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'style', 'painter', 'content', 'photo', 'get_html_photo', 'is_published')
    readonly_fields = ('is_published', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Pictures"


class StylesAdmin(admin.ModelAdmin):
    list_display = ('id', 'style_name')
    list_display_links = ('id', 'style_name')
    search_fields = ('style_name',)


class PainterAdmin(admin.ModelAdmin):
    list_display = ('id', 'painter_name', 'get_html_painter_photo', 'painter_content')
    list_display_links = ('id', 'painter_name')
    search_fields = ('painter_name', 'painter_content')
    #fields = ('id', 'painter_name', 'get_html_painter_photo', 'painter_content')
    save_on_top = True

    def get_html_painter_photo(self, object):
        if object.painter_photo:
            return mark_safe(f"<img src='{object.painter_photo.url}' width=50>")

    get_html_painter_photo.short_description = "Pictures"


admin.site.register(Article, ArticleAdmin)
admin.site.register(Styles, StylesAdmin)
admin.site.register(Painters, PainterAdmin)

admin.site.site_title = 'Admin-page Art&Clue'
admin.site.site_header = 'Admin-page Art&Clue'
