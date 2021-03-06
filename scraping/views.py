from django.shortcuts import render
from .models import Vacancy

def index(request):
    qs = Vacancy.objects.all()
    return render(request, 'scraping/index.html', {'object_list': qs})

def vacancys(request):
    qs = Vacancy.objects.all()
    return render(request, 'scraping/vacancys.html', {'object_list': qs})
