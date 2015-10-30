from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.site_login, name='site_login'),
    url(r'^register/$', views.site_register, name='site_register'),
    url(r'^logout/$', views.site_logout, name='site_logout'),
]