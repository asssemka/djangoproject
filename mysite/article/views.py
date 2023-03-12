from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import *
from .forms import *

# Create your views here.
# def index(request):
#      return render(request, 'article/index.html')
class ArticleHome(ListView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Article.objects.filter(is_published=True)
# def index(request):
#     posts = Article.objects.all()
#     styles = Styles.objects.all()
#
#     context = {
#         'posts': posts,
#         'styles': styles,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'article/index.html', context=context)

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

class AddPage (CreateView):
    form_class = AddPostForm
    template_name = 'article/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        return context

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             try:
#                 Article.objects.create(**form.cleaned_data)
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления поста')
#
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи'})

class ArticleCategory(ListView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Article.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context

# def show_category(request, style_id):
#     posts = Article.objects.filter(style_id=style_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': style_id,
#     }
#
#     return render(request, 'article/index.html', context=context)
class ShowPost(DetailView):
    model = Article
    template_name = 'article/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        return context