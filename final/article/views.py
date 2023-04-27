from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
import django_filters
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, viewsets, mixins
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import ArticleSerializer

from .models import *
from .forms import *
from .utils import DataMixin


# Create your views here.
# def index(request):
#      return render(request, 'article/index.html')
def error404(request, exeption):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")


def error500(request):
    return HttpResponseNotFound("<h1>Ошибка сервера</h1>")


def error400(request, exeption):
    return HttpResponseNotFound("<h1>Некорректный запрос</h1>")


def error403(request, exeption):
    return HttpResponseNotFound("<h1>Доступ запрещен</h1>")


class ArticleHome(DataMixin, ListView):
    paginate_by = 3
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        styles = Styles.objects.all()
        context['styles'] = styles
        print(styles)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related('style')


class ArticleStyle(DataMixin, ListView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Article.objects.filter(style__slug=self.kwargs['style_slug'], is_published=True).select_related('style')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g = get_object_or_404(Styles, slug=self.kwargs['style_slug'])
        g_def = self.get_user_context(title='Стиль - ' + str(g.style_name),
                                      style_selected=g.pk)
        return dict(list(context.items()) + list(g_def.items()))


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


class ShowArticle(DataMixin, DetailView):
    model = Article
    template_name = 'article/article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        article = self.get_object()
        comments = Comments.objects.filter(article=article.id)
        context['form'] = CommentForm()
        context['comments'] = comments
        likes = Like.objects.filter(article=article.id)
        context['likes'] = likes
        g_def = self.get_user_context(title=context['article'])

        # user = self.request.user
        return dict(list(context.items()) + list(g_def.items()))


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    form_class = CommentForm

    # template_name = 'comment_form.html'

    # success_url = reverse_lazy('index')

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.article = article
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        article_slug = self.object.article.slug
        success_url = reverse('show_article', kwargs={'article_slug': article_slug})
        return success_url


def like_article(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    likes = Like.objects.filter(article=article.id)
    if request.user.is_authenticated and not likes.filter(user=request.user).exists():
        # like = Like(user=request.user, article=article)
        like = Like()
        like.user = request.user
        like.article = article
        like.save()
    elif request.user.is_authenticated and likes.filter(user=request.user).exists():
        like = Like.objects.get(user_id=request.user.id, article=article.id)
        like.delete()

    return redirect('show_article', article_slug=article.slug)


class ArticleSearch(DataMixin, ListView):
    model = Article
    template_name = 'article/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        article = Article.objects.filter(
            Q(title__icontains=query) | Q(title__icontains=query)
        )
        return article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Поиск: " + self.request.GET.get('q'))
        return dict(list(context.items()) + list(g_def.items()))


# def article_search(request):
#     query = request.GET.get('q')
#     article = Article.objects.filter(title__icontains=query)
#     return render(request, 'article_search.html', {'article': article})


class Painters(DataMixin, ListView):
    paginate_by = 3
    model = Painters
    template_name = 'article/painters.html'
    context_object_name = 'painters'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    # def get_queryset(self):
    #     return Painters.objects.filter(is_published=True)


class ShowPainter(DataMixin, DetailView):
    model = Painters
    template_name = 'article/painter.html'
    slug_url_kwarg = 'painter_slug'
    context_object_name = 'painter'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        painter = self.get_object()
        g_def = self.get_user_context(title=context['painter'])

        # user = self.request.user
        return dict(list(context.items()) + list(g_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'article/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))


def about(request):
    return render(request, 'article/about.html')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1/>')


def profile(request):
    return render(request, 'article/profile.html')


class UserProfile(DataMixin, DetailView):
    model = CustomUser
    template_name = "article/profile.html"
    username_url_kwarg = 'username'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return CustomUser.objects.get(username=self.kwargs['username'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user'] = user
        g_def = self.get_user_context(title=context['user'])

        return dict(list(context.items()) + list(g_def.items()))


class EditUserProfile(DataMixin, UpdateView):
    model = CustomUser
    template_name = "article/edit_profile.html"
    fields = ['first_name', 'last_name', 'username', 'email', 'avatar']

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('profile', kwargs={'user_username': username})

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['first_name'].widget.attrs.update({'class': 'form-input'})
        form.fields['last_name'].widget.attrs.update({'class': 'form-input'})
        form.fields['username'].widget.attrs.update({'class': 'form-input'})
        form.fields['email'].widget.attrs.update({'class': 'form-input'})
        return form

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user'] = user
        g_def = self.get_user_context(title="Редактирование профиля")


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'article/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'article/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('profile')


def logout_user(request):
    logout(request)
    return redirect('login_user_page')


# class ArticleViewSet(mixins.CreateModelMixin,
#                      mixins.RetrieveModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.ListModelMixin,
#                      GenericViewSet):
#     #queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#
#     def get_queryset(self):
#         return Article.objects.all()[:3]
#
#     @action(methods=['get'], detail=True)
#     def style(self, request, pk=None):
#         style = Styles.objects.get(pk=pk)
#         return Response({'style': style.style_name})
#
#     @action(methods=['get'], detail=True)
#     def painter(self, request, pk=None):
#         painter = Painters.objects.get(pk=pk)
#         return Response({'painter': painter.painter_name})

class ArticleAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2


class ArticleAPIList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = ArticleAPIListPagination


class ArticleAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication, )


class ArticleAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAdminOrReadOnly,)
