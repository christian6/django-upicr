from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.db import connection, transaction
from django.views.generic import View, DetailView
from django.utils import simplejson

"""
###
# 	Renderizar fetchall para los templates
###
"""
def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

def ValidKeyCotizacion(request):
	if request.method == 'POST':
		cn = connection.cursor()
		cn.execute("SELECT COUNT(*) FROM logistica.autogenerado WHERE rucproveedor LIKE '"+request.session.get('rucpro')+"' AND nrocotizacion LIKE '"+request.POST['nro']+"' AND keygen LIKE '"+request.POST['key']+"' AND esid LIKE '14'")
		count = 0
		data = ''
		count = cn.fetchone()
		print count[0]
		if count[0] == 0:
			data = '{ "status" : "error" }'
		elif count[0] == 1:
			data = '{ "status" : "success", "ncot" : "'+request.POST['nro']+'" }'
		data = simplejson.dumps(data)
		return HttpResponse(data,mimetype='application/json')

@transaction.commit_manually
def update_price_quote(request):
	if request.method == 'POST':
		cn = connection.cursor()
		cn.execute("UPDATE logistica.detcotizacion SET precio = "+request.POST['pre']+" WHERE nrocotizacion LIKE '"+request.POST['nro']+"' AND rucproveedor LIKE '"+request.session.get('rucpro')+"' AND materialesid LIKE '"+request.POST['mat']+"'")
		transaction.commit()
		cn.close()
		data = '{ "status" : "success" }'
		data = simplejson.dumps(data)
		return HttpResponse(data,mimetype='application/json')

@transaction.commit_manually
def update_date_quote(request):
	if request.method == 'POST':
		cn = connection.cursor()
		cn.execute("UPDATE logistica.detcotizacion SET fecent = '"+request.POST['fec']+"'::date WHERE nrocotizacion LIKE '"+request.POST['nro']+"' AND rucproveedor LIKE '"+request.session.get('rucpro')+"' AND materialesid LIKE '"+request.POST['mat']+"'")
		transaction.commit()
		cn.close()
		data = '{ "status" : "success" }'
		data = simplejson.dumps(data)
		return HttpResponse(data,mimetype='application/json')

@transaction.commit_manually
def update_mark_quote(request):
	if request.method == 'POST':
		cn = connection.cursor()
		cn.execute("UPDATE logistica.detcotizacion SET marca = '"+request.POST['mar']+"' WHERE nrocotizacion LIKE '"+request.POST['nro']+"' AND rucproveedor LIKE '"+request.session.get('rucpro')+"' AND materialesid LIKE '"+request.POST['mat']+"'")
		transaction.commit()
		cn.close()
		data = '{ "status" : "success" }'
		data = simplejson.dumps(data)
		return HttpResponse(data,mimetype='application/json')

def upload_tecnica_quote(request):
	if request.method == 'POST':
		import os
		from django.conf import settings
		path = settings.PATH_PROJECT
		cot = 'media/store/cotizacion/'+request.POST['nro']+'/H_TECNICAS/'
		pathabs = os.path.join(path,cot)
		if not os.path.exists(pathabs):
			os.makedirs(pathabs,0777)

		f = request.FILES['arch']
		pathabs+=request.POST['mat']+'.pdf'
		destination = open(pathabs, 'wb+')
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close()
		data = '{ "status" : "success"}'
		data = simplejson.dumps(data)
		return HttpResponse(data,mimetype='application/json')

@transaction.commit_manually
def saved_cotizacion_customer(request):
	if request.method == 'POST':
		data = '{ "status" : "success" }'
		try:
			cn = connection.cursor()
			cn.execute("INSERT INTO logistica.cotizacioncli(nrocotizacion,rucproveedor,fecenv,contacto,fval,monedaid,obser,esid) VALUES('"+request.POST['nro']+"', '"+request.session.get('rucpro')+"', '"+request.POST['fen']+"'::date, '"+request.POST['con']+"', '"+request.POST['fva']+"'::date, '"+request.POST['mon']+"', '"+request.POST['obs']+"','11')")
			transaction.set_dirty()
			transaction.commit()
			cn.close()
		except Exception, e:
			transaction.rollback()
			data = '{ "status" : "fail" }'

		try:
			arch = request.POST['arch']
		except Exception, e:
			arch = 'files'
			raise e

		if arch != 'nothing':
			import os
			from django.conf import settings
			path = settings.PATH_PROJECT
			cot = 'media/store/cotizacion/'+request.POST['nro']+'/'
			pathabs = os.path.join(path,cot)
			if not os.path.exists(pathabs):
				os.makedirs(pathabs,777)
				os.chmod(pathabs,777)

			f = request.FILES['arch']
			pathabs+='adj'+request.POST['nro']+'.'+request.POST['ext']
			destination = open(pathabs, 'wb+')
			for chunk in f.chunks():
				destination.write(chunk)
			destination.close()

			data = simplejson.dumps(data)
		
		return HttpResponse(data, mimetype='application/json')