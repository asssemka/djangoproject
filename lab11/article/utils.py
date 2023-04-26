from django.db.models import Count
from django.core.cache import cache
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        style = cache.get('style')
        # style = Styles.objects.annotate(Count('article'))
        if not style:
            style = Styles.objects.annotate(Count('article'))
            cache.set('style', style, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['style'] = style
        if 'style_selected' not in context:
            context['style_selected'] = 0
        return context
