from django import template
from article.models import *

register = template.Library()

@register.simple_tag(name='getstyles')
def get_styles(filter=None):
    if not filter:
        return Styles.objects.all()
    else:
        return Styles.objects.filter(pk=filter)

@register.inclusion_tag('article/list_categories.html')
def show_styles(sort=None, style_selected=0):
    if not sort:
        styles = Styles.objects.all()
    else:
        styles = Styles.objects.order_by(sort)

    return {"styles": styles, "style_selected": style_selected}
