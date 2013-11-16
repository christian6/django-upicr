from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('icrperu.apps.logistica.views',
	url(r'^$','view_index',name='vw_logistica_home'),
	#url(r'^security/login/(?P<dni>\d+)/nom/(?P<nom>\S+)/res$','view_securitylog',name='vw_securitylog'),
	## Login and Logout
	url(r'^security/login/$','view_securitylog',name='vw_securitylog'),
	url(r'^security/logout/$','view_logout',name='vw_logout'),
	## Suministro
	url(r'^suministro/aprobar/$','view_aprobarsuministro',name='vw_aprobar_suministro'),
	url(r'^cotizacion/suministro/$','view_cotiza_suministro',name='vw_cotiza_suministro'),
	## Cotizacion
	url(r'^cotizacion/materiales/simple/$','view_cotizacion_simple',name='vw_cotizacion_simple'),
	url(r'^list/cotizacion/$','view_list_cotizacion',name='vw_list_cotizacion'),
	url(r'^compare/supplier/(?P<nro>.*)/$','view_compare_supplier',name='vw_compare_supplier'),
)