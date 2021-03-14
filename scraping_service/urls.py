
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from users import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('scraping.urls')),
    url(r'', include(('users.urls', 'users'))),
]
