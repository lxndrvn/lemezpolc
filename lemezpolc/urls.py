from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.release_list, name='index'),
]
