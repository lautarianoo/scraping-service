
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from scraping.views import VDetail, VUpdate

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('scraping.urls')),
    url(r'', include(('users.urls', 'users'))),
    path('update/<int:pk>/', VUpdate.as_view(), name='update'),
    path('detail/<int:pk>/', VDetail.as_view(), name='detail')
]
