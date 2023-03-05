from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from article.models import Article, Styles


# Create your views here.
# def index(request):
#      return render(request, 'article/index.html')
def index(request):
    posts = Article.objects.all()
    styles = Styles.objects.all()

    context = {
        'posts': posts,
        'styles': styles,
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    return render(request, 'article/index.html', context=context)

def about(request):
     return render(request, 'article/about.html')


def categories(request, catid):
     if(request.GET):
          print(request.GET)

     return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


def archive(request, year):
     if int(year) > 2020:
          return redirect('/', permanent=True)

     return HttpResponse(f"<h1>Архив по годам</h1>{year}</p>")

def pageNotFound(request, exception):
     return HttpResponseNotFound('<h1>Страница не найдена<h1/>')

def show_post(request, post_slug):
    post = get_object_or_404(Article, slug=post_slug)

    context = {
        'post': post,
        'title': post.title,
        'cat_selected': post.style_id,
    }

    return render(request, 'article/post.html', context=context)

def show_category(request, style_id):
    posts = Article.objects.filter(style_id=style_id)

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'title': 'Отображение по рубрикам',
        'cat_selected': style_id,
    }

    return render(request, 'article/index.html', context=context)