from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('', 
    url(r'^$', views.index, name='index'),
    url(r'^bypass/', views.bypass, name='bypass'),
    url(r'^(?P<host>[A-Za-z0-9._]+)/$',
            views.host_series, name='host_series'),
    url(r'^(?P<host>[A-Za-z0-9._]+)/(?P<service>[A-Za-z0-9._]+)/$',
            views.service_series, name='service_series'),
    url(r'^(?P<host>[A-Za-z0-9._]+)/(?P<service>[A-Za-z0-9._]+)/(?P<series>[A-Za-z0-9._]+)/$',
            views.simple_series, name='simple_series'),
)
