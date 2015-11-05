from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^delete/', views.delete_content, name='delete_content'),
    url(r'^view/profile/([0-9]+)/$', views.view_content_profile, name='view_content_profile'),
    url(r'^view/circle/([0-9]+)/$', views.view_content_circle, name='view_content_circle'),
]