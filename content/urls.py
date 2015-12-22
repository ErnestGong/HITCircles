from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^delete/', views.delete_content, name='delete_content'),
    url(r'^view/profile/([0-9]+)/$', views.view_content_profile, name='view_content_profile'),
    # url(r'^view/circle/([0-9]+)/$', views.view_content_circle, name='view_content_circle'),
    url(r'^view/follower/([0-9]+)/$', views.check_follower, name='view_follower'),
    url(r'^view/followed/([0-9]+)/$', views.check_followed, name='view_followed'),
    url(r'^view/thumb_up/$', views.process_thumb_up, name='process_thumb_up'),
    url(r'^view/show_comment/$', views.show_comment, name='show_comment'),
    url(r'^view/add_comment/$', views.add_comment, name='add_comment'),
]