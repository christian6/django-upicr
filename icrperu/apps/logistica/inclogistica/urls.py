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
	url(r'^search/key/cotizacion/$','wv_search_key_cotizacion'),
	url(r'^upload/template/cotizacion/simple/$','ws_upload_reade_cotizacion_simple'),
	# Compare
	url(r'^compare/supplier/cotizacion/$','ws_compare_supplier',name='inc_compare_supplier'),
	url(r'^consulting/money/supplier/$','ws_obtener_money_supplier',name='inc_obtener_money_supplier'),
	url(r'^consulting/mat/buy/$','ws_obtener_det_mat_buy'),
	url(r'^save/order/buy/$','ws_save_order_buy'),
	url(r'^change/status/cotizacion/$','wv_change_status_cotizacion'),
	url(r'^update/anular/quotation/$','ws_update_anular_quotation'),
	url(r'^update/anular/buy/$','ws_update_anular_buy'),
	# Compra
	url(r'^list/tmp/compra/$','ws_list_tmp_compra'),
	url(r'^delete/tmp/det/buy/$','ws_delete_tmp_det_buy'),
	url(r'^add/tmp/detils/buy/$','ws_add_tmp_detils_buy'),
	url(r'^edit/mat/tmp/buy/$','ws_edit_mat_tmp_buy'),
	url(r'^delete/mat/tmp/compra/$','ws_delete_mat_tmp_buy'),
	url(r'^upload/ready/buy/tmp/$','ws_upload_ready_buy_tmp'),
	url(r'^saved/order/buy/single/$','ws_saved_order_buy_single'),
	# General
	url(r'^search/departamento/$','ws_search_departamento'),
	url(r'^search/provincia/$','ws_search_provincia'),
	url(r'^search/distrito/$','ws_search_distrito'),
	url(r'^save/supplier/$','ws_save_supplier'),
	url(r'^delete/supplier/$','ws_delete_supplier'),
	url(r'^saved/login/supplier/$','ws_saved_login_supplier'),
	url(r'^consulting/order/buy/$','ws_consulting_order_buy'),
	url(r'^upload/file/stock/$','ws_upload_file_stock'),
	# -- Tipo de Cambio --
	url(r'^consulting/type/change/money/$','ws_type_change_money'),
	
)