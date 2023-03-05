from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('style/<int:style_id>/', show_category, name='category'),
]




