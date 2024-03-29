from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    # path('', cache_page(60)(ArticleHome.as_view()), name='home'),
    path('', ArticleHome.as_view(), name='home'),
    path('article/<slug:article_slug>/', ShowArticle.as_view(), name="show_article"),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('about/', about, name='about'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    # path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    #path('style/<slug:style_slug>/', ArticleCategory.as_view(), name='style'),
]




