from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('icrperu.apps.logistica.inclogistica.views',
	# Consulta de Suministro
	url(r'^list/suministro/$','ws_list_suministro',name='inc_suminsitro_nro'),
	url(r'^listdet/suministro/$','ws_det_suminsitro',name='inc_detsuministro'),
	url(r'^update/approved/suministro/$','ws_approved_suministro',name='inc_approved_suministro'),
	url(r'^update/annulled/suministro/$','ws_annulled_suministro',name='inc_annulled_suministro'),
	url(r'^list/det/suministro/$','ws_det_suministro_cot',name='inc_cot_det_suministro'),
	# De Suministro a Cotizacion
	url(r'^save/cotizacion/$','ws_save_cotizacion',name='inc_save_cotizacion'),
	url(r'^save/cotizacion/proveedor/$','ws_cotiza_proveedor',name='inc_save_cotiza_proveedor'),
	url(r'^finally/cotiza/suministro/$','ws_finalize_cotiza_sum',name='inc_finally_cotiza_sum'),
	# Cotizacion Simple
	url(r'^consulta/medida/material/$','ws_consulta_det_mat',name='inc_medida_mat'),
	url(r'^consulta/detalle/material/$','ws_consulta_data_det',name='inc_detalle_mat'),
	url(r'^consulta/detalle/tmp/cotiza/$','ws_lista_detalle_cotiza',name='inc_tmp_cotiza'),
	url(r'^delete/tmp/cotiza/$','ws_del_tmp_cotiza',name='inc_delete_tmp_cotiza'),
	url(r'^add/tmp/cotiza/$','ws_add_tmp_cotiza',name='inc_add_tmp_cotiza'),
	url(r'^delete/mat/tmp/cotiza/$','ws_del_mat_tmp_cotiza',name='inc_del_mat_tmp_cotiza'),
	url(r'^edit/mat/tmp/cotiza/$','ws_edit_mat_tmp_cotiza',name='inc_edit_mat_tmp_cotiza'),
	url(r'^save/cotiza/simple/$','ws_save_cotizacion_simple',name='inc_save_cotiza_simple'),
	url(r'^lista/tmp/material/cotiza/$','ws_list_tmp_cotiza',name='inc_lista_tmp_cotiza'),
	url(r'^save/proveedor/cotizacion/simple/$','ws_cotiza_proveedor_simple',name='inc_save_proveedor_cotiza_simple'),
	url(r'^finish/cotizacion/simple/$','ws_finish_cotiza_proveedor_simple',name='inc_finish_cotiza_simple'),
)