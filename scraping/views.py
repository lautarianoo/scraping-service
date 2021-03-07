from django.shortcuts import render
from .models import Vacancy
from .forms import FindVac

def index(request):
    city = request.GET.get('city')
    prof = request.GET.get('prof')
    qs = []
    if city or prof:
        _filter = {}
        if city:
            _filter['city__name'] = city
        if prof:
            _filter['prof__name'] = prof
        qs = Vacancy.objects.filter(**_filter)
    return render(request, 'scraping/index.html', {'object_list': qs})

def vacancys(request):
    city = request.GET.get('city')
    prof = request.GET.get('prof')
    qs = []
    if city or prof:
        _filter = {}
        if city:
            _filter['city__name'] = city
        if prof:
            _filter['prof__name'] = prof
        qs = Vacancy.objects.filter(**_filter)
    else:
        qs = Vacancy.objects.all()
    return render(request, 'scraping/vacancys.html', {'object_list': qs})
