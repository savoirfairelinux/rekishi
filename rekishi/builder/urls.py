from django.conf.urls import patterns, url

from rekishi.builder import views

urlpatterns = patterns('', 
    url(r'^$', views.index, name='index'),
)

