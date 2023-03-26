from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import *
from .forms import *
from .utils import DataMixin


# Create your views here.
# def index(request):
#      return render(request, 'article/index.html')


class ArticleHome(DataMixin, ListView):
    paginate_by = 3
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'article/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))




# class ShowPost(DataMixin, DetailView):
#     model = Article
#     template_name = 'article/post.html'
#     slug_url_kwarg = 'post_slug'
#     context_object_name = 'post'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title=context['post'])
#         return dict(list(context.items()) + list(c_def.items()))



def about(request):
    contact_list = Article.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'article/about.html', {'page_obj': page_obj, 'title': 'О сайте'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1/>')