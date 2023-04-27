from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    # path('', cache_page(60)(ArticleHome.as_view()), name='home'),
    path('', cache_page(60)(ArticleHome.as_view()), name='home'),
    path('painters/', cache_page(60)(Painters.as_view()), name='painters'),
    path('article/<slug:article_slug>/', ShowArticle.as_view(), name="show_article"),
    path('painter/<slug:painter_slug>/', ShowPainter.as_view(), name="show_painter"),
    path('style/<slug:style_slug>/', ArticleStyle.as_view(), name='style'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('about/', about, name='about'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login_user/', LoginUser.as_view(), name='login_user_page'),
    path('logout_user/', logout_user, name='logout_user_page'),
    path('profile/', profile, name='profile'),
    path('article_search/', ArticleSearch.as_view(), name='article_search'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='create_comment'),
    path('/like_article/<int:article_pk>', like_article, name='like_article'),
    #path('user/<str:user_username>/editprofile', EditUserProfile.as_view(), name="editprofile"),
    # path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    #path('style/<slug:style_slug>/', ArticleCategory.as_view(), name='style'),
]




