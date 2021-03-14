from django.conf.urls import url
from django.urls import path
from users.views import login_view, logout_view, register_view, update_view, delete_view

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', register_view, name='register'),
    url(r'^update/$', update_view, name='update'),
    url(r'^delete/$', delete_view, name='delete')
]