from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ArticleSerializer, PainterSerializer

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
        return Article.objects.filter(is_published=True).select_related('style')


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
        g_def = self.get_user_context(title=context['article'])
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
    contact_list = Article.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'article/about.html', {'page_obj': page_obj, 'title': 'О сайте'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1/>')


def profile(request):
    return render(request, 'article/profile.html')


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
    return redirect('login')


class ArticleAPIView(APIView):
    def get(self, request):
        a = Article.objects.all()
        return Response({'posts': ArticleSerializer(a, many=True).data})

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Article.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = ArticleSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            article = Article.objects.get(pk=pk)
            article.delete()
        except:
            return Response({"error": "Object does not exists"})

        return Response({"post": "delete post " + str(pk)})

# class ArticleAPIView(generics.ListAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


# class PaintersAPIView(generics.ListAPIView):
#     queryset = Painters.objects.all()
#     serializer_class = PainterSerializer

class PaintersAPIView(APIView):
    def get(self, request):
        p = Painters.objects.all()
        return Response({'posts': PainterSerializer(p, many=True).data})

    def post(self, request):
        serializer = PainterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer = PainterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Painters.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = PainterSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            painter = Painters.objects.get(pk=pk)
            painter.delete()
        except:
            return Response({"error": "Object does not exists"})

        return Response({"post": "delete post " + str(pk)})