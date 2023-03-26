from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('', ArticleHome.as_view(), name='home'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('about/', about, name='about'),
    # path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # path('category/<slug:cat_slug>/', ArticleCategory.as_view(), name='category'),
]




