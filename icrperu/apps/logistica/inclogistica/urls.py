from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('icrperu.apps.logistica.inclogistica.views',
	url(r'^list/suministro/$','ws_list_suministro',name='inc_suminsitro_nro'),
	url(r'^listdet/suministro/$','ws_det_suminsitro',name='inc_detsuministro'),
	url(r'^update/approved/suministro/$','ws_approved_suministro',name='inc_approved_suministro'),
	url(r'^update/annulled/suministro/$','ws_annulled_suministro',name='inc_annulled_suministro'),
	url(r'^list/det/suministro/$','ws_det_suministro_cot',name='inc_cot_det_suministro'),
)