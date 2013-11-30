from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('icrperu.apps.proveedor.views',
	# 
	url(r'^$','view_index_supplier',name='vw_index_supplier'),
	## Login and Logout
	url(r'^security/login/$','view_login_supplier',name='vw_securitylog'),
	url(r'^security/logout/$','view_logout_supliert',name='vw_logout_supliert'),
	# Proveedores
	url(r'^home/','view_home_supplier',name='vw_home_supplier'),
	# Cotizaciones
	url(r'^list/cotizaciones/$','view_list_cotizaciones_supplier',name='vw_list_cotizacion_supplier'),
	url(r'^view/cotizacion/(?P<nro>.*)/$','view_cotizacion_supplier',name='vw_cotizacion_supplier'),
	#Ordenes de Compra
	url(r'^lista/compra/$','view_list_Order_buy',name='vw_list_Order_buy'),
)