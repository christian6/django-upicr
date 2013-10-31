from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('icrperu.apps.proveedor.views',
	# 
	url(r'^$','view_index',name='vw_logistica_home'),
	## Login and Logout
	url(r'^security/login/$','view_securitylog',name='vw_securitylog'),
	# Proveedores
	url(r'^home/','view_home',name='vw_home'),
)