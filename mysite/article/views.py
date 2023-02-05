from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
     return HttpResponse("Страница приложения article")

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

