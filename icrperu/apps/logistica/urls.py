from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('icrperu.apps.logistica.views',
	url(r'^$','view_index',name='vw_logistica_home'),
	url(r'^security/login/(?P<dni>.*)/(?P<nombre>.*)/(?P<cargo>.*)/$','view_securitylog',name='vw_securitylog'),
)