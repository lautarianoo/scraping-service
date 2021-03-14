from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy
from .forms import FindVac

def index(request):
    city = request.GET.get('city')
    prof = request.GET.get('prof')
    page_obj = []
    context = {'city': city, 'prof': prof}
    if city or prof:
        _filter = {}
        if city:
            _filter['city__name'] = city
        if prof:
            _filter['prof__name'] = prof
        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
        context['len'] = len(qs)
    return render(request, 'scraping/index.html', context)

def vacancys(request):
    city = request.GET.get('city')
    prof = request.GET.get('prof')
    page_obj = []
    context = {'city': city, 'prof': prof}
    if city or prof:
        _filter = {}
        if city:
            _filter['city__name'] = city
        if prof:
            _filter['prof__name'] = prof
        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
        context['len'] = len(qs)
    else:
        qs = Vacancy.objects.all()
        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/vacancys.html', context)
