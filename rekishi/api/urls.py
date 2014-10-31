from django.conf.urls import patterns, url

from rekishi.api import views

urlpatterns = patterns('', 
    # url(r'^bypass/', views.bypass, name='bypass'),
    url(r'dg/(?P<host>[A-Za-z0-9._]+)/$',
           views.dg_host_series, name='dg_host_series'),
    url(r'dg/(?P<host>[A-Za-z0-9._]+)/(?P<service>[A-Za-z0-9._]+)/$',
            views.dg_service_series, name='dg_service_series'),
    url(r'dg/(?P<host>[A-Za-z0-9._]+)/(?P<service>[A-Za-z0-9._]+)/(?P<series>[A-Za-z0-9._]+)/$',
            views.dg_single_series, name='dg_single_series'),
)
