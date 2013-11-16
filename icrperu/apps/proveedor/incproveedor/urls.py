from django.conf.urls.defaults import patterns, url
#from icrperu.apps.proveedor.incproveedor import views

urlpatterns = patterns('icrperu.apps.proveedor.incproveedor.views',
	url(r'^consulting/key/valid/$','ValidKeyCotizacion',name='vw_valid_key_cotiza'),
	url(r'^update/price/quote/$','update_price_quote',name='vw_update_price_quote'),
	url(r'^update/date/quote/$','update_date_quote',name='vw_update_date_quote'),
	url(r'^update/mark/quote/$','update_mark_quote',name='vw_update_mark_quote'),
	url(r'^upload/file/quote/$','upload_tecnica_quote',name='vw_upload_file_quote'),
	url(r'^saved/cotizacion/customer/$','saved_cotizacion_customer',name='vw_saved_cotizacion_customer'),
)