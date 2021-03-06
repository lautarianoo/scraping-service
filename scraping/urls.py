from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.vacancys, name='vacancys')
]