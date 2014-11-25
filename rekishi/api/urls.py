

from django.conf.urls import patterns, url

from rekishi.api import views
from rekishi.api.response_builder import dygraph_response_wrapper


urlpatterns = patterns('', 
    # url(r'^bypass/', views.bypass, name='bypass'),

    url(r'dg/(?P<host>.+?)/(?P<service>.+?)/(?P<serie>.+?)/$',
            dygraph_response_wrapper(views.host.dg_single_series), name='dg_single_serie'),

    url(r'dg/(?P<host>.+?)/(?P<service>.+?)/$',
            dygraph_response_wrapper(views.host.dg_service_series), name='dg_service_series'),

    url(r'dg/(?P<host>.+?)/$',
           dygraph_response_wrapper(views.host.dg_host_series), name='dg_host_series'),

)
