"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from article import views
from article.views import *
from mysite import settings
from rest_framework import routers


# class MyCustomRouter(routers.SimpleRouter):
#     routes = [
#         routers.Route(
#             url=r'^{prefix}$',
#             mapping={'get': 'list'},
#             name='{basename}-list',
#             detail=False,
#             initkwargs={'suffix': 'List'}
#         ),
#         routers.Route(
#             url=r'^{prefix}/{lookup}$',
#             mapping={'get': 'retrieve'},
#             name='{basename}-detail',
#             detail=True,
#             initkwargs={'suffix': 'Detail'}
#         ),
#         routers.Route(
#             url=r'^{prefix}/$',
#             mapping={'get': 'list'},
#             name='{basename}-default',
#             detail=False,
#             initkwargs={'suffix': 'Default'}
#         ),
#     ]
#

# router = routers.DefaultRouter()
# router.register(r'article', ArticleViewSet, basename='article')
# print(router.urls)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('article.urls')),
    path('captcha/', include('captcha.urls')),
    path('api/v1/article/', ArticleAPIList.as_view()),
    path('api/v1/article/<int:pk>/', ArticleAPIUpdate.as_view()),
    path('api/v1/articledelete/<int:pk>/', ArticleAPIDestroy.as_view()),
    #path('api/v1/', include(router.urls)),  # http://127.0.0.1:8000/api/v1/women/


]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
