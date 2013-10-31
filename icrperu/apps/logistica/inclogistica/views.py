#!-*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.db import connection, transaction
#from django.core import serializers

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

"""
###
# Logistica Suministro
###
"""

def ws_list_suministro(request):
	if request.method == 'GET':
		prm = ''
		try:
			if request.GET['type'] == 'nro':
				prm = "s.nrosuministro LIKE '%s'"%(request.GET['nro'])
			elif request.GET['type'] == 'fi':
				prm = "s.fecha::date = '%s'::date "%(request.GET['fi'])
			elif request.GET['type'] == 'ff':
				prm = "s.fecha::date BETWEEN '%s'::date AND '%s'::date "%(request.GET['fi'],request.GET['ff'])
		except Exception, e:
			raise e
		
		cn = connection.cursor()
		cn.execute("SELECT s.nrosuministro,a.descri,e.empnom,s.fecha::date,s.fecreq,d.esnom FROM almacen.suministro s INNER JOIN admin.almacenes a ON s.almacenid=a.almacenid INNER JOIN admin.empleados e ON s.empdni=e.empdni INNER JOIN admin.estadoes d ON s.esid LIKE d.esid WHERE s.esid LIKE '40' AND "+prm+" ORDER BY nrosuministro ASC")
		lista = cn.fetchall()
		data = ""
		i = 0
		for k in lista:
			i = (i + 1)
			data += "<tr>"
			data += "<td>"+str(i)+"</td>"
			data += "<td>"+str(k[0])+"</td>"
			data += "<td>"+str(k[1])+"</td>"
			data += "<td>"+str(k[2])+"</td>"
			data += "<td>"+str(k[3])+"</td>"
			data += "<td>"+str(k[4])+"</td>"
			data += "<td>"+str(k[5])+"</td>"
			data += "<td><button class='btn btn-primary btn-xs' onClick=getdetail('"+k[0]+"');><span class='glyphicon glyphicon-list'></span></button></td>"
			data += "</tr>"

		data += "|success"
		#data = serializers.serialize('json',dictfetchall(cn))
		return HttpResponse(data,mimetype='application/html')

def ws_det_suminsitro(request):
	if request.method == 'GET':
		data = ''
		try:
			cn = connection.cursor()
			cn.execute("SELECT DISTINCT d.materialesid,m.matnom,m.matmed,m.matund,SUM(d.cantidad) as cantidad FROM almacen.suministro s INNER JOIN almacen.detsuministro d ON s.nrosuministro LIKE d.nrosuministro INNER JOIN admin.materiales m ON d.materialesid LIKE m.materialesid WHERE s.nrosuministro LIKE '"+request.GET['nro']+"' GROUP BY d.materialesid,m.matnom,m.matmed,m.matund ")
			lista = cn.fetchall()
			for x in lista:
				data += "<tr class='success'>"
				data += "<td>"+str(x[0])+"</td>"
				data += "<td>"+x[1]+"</td>"
				data += "<td>"+x[2]+"</td>"
				data += "<td>"+str(x[3])+"</td>"
				data += "<td>"+str(x[4])+"</td>"
				data += "</tr>"
		except Exception, e:
			raise e
		return HttpResponse(data,mimetype="application/json")

@transaction.commit_manually
def ws_approved_suministro(request):
	if request.method == 'GET':
		data = ''
		cn = connection.cursor()
		cn.execute("UPDATE almacen.suministro SET esid = '38' WHERE nrosuministro LIKE '"+request.GET['nro']+"'")
		transaction.set_dirty()
		transaction.commit()
		data = 'success'

		return HttpResponse(data,mimetype="application/json")

@transaction.commit_manually
def ws_annulled_suministro(request):
	if request.method == 'GET':
		data = ''
		cn = connection.cursor()
		cn.execute("UPDATE almacen.suministro SET esid = '39' WHERE nrosuministro LIKE '"+request.GET['nro']+"'")
		transaction.set_dirty()
		transaction.commit()
		data = 'success'
		return HttpResponse(data,mimetype="application/json")
"""
####
## 	Cotizacion de una Orden de Suministro
####
"""
def ws_det_suministro_cot(request):
	if request.method == 'GET':
		data = ''
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT d.materialesid,m.matnom,m.matmed,m.matund,SUM(d.cantidad) as cantidad FROM almacen.suministro s INNER JOIN almacen.detsuministro d ON s.nrosuministro LIKE d.nrosuministro INNER JOIN admin.materiales m ON d.materialesid LIKE m.materialesid WHERE s.nrosuministro LIKE '"+request.GET['nro']+"' GROUP BY d.materialesid,m.matnom,m.matmed,m.matund ")
		lista = cn.fetchall()
		i = 1
		for x in lista:
			data += "<tr class='success'>"
			data += "<td>"+str(i)+"</td>"
			data += "<td>"+str(x[0])+"</td>"
			data += "<td>"+str(x[1])+"</td>"
			data += "<td>"+x[2]+"</td>"
			data += "<td>"+str(x[3])+"</td>"
			data += "<td>"+str(x[4])+"</td>"
			data += "<td><input type='checkbox' name='mat' value='"+str(x[0])+"' /></td>"
			data += "</tr>"
			i += 1

		return HttpResponse(data,mimetype='application/json')

@transaction.commit_manually
def ws_save_cotizacion(request):
	if request.is_ajax():
		data = 'success'
		# obteniendo nro de cotizacion
		cn = connection.cursor()
		cn.execute("SELECT * FROM logistica.spnuevacotizacion()")
		cot = cn.fetchone()
		cn.close()
		# guardando cotizacion
		#print cot[0]
		cn = connection.cursor()
		cn.execute("INSERT INTO logistica.cotizacion VALUES('"+cot[0].strip()+"','"+request.GET['dni']+"',now(),'"+request.GET['fec']+"'::date,'"+request.GET['obs']+"','14' )")
		transaction.set_dirty()
		transaction.commit()
		cn.close()
		# sumcot
		cn = connection.cursor()
		cn.execute("INSERT INTO almacen.sumcot VALUES('"+request.GET['nro']+"','"+cot[0].strip()+"');")
		transaction.set_dirty()
		transaction.commit()
		cn.close()
		return HttpResponse(data,mimetype='application/html')

def generateKey():
	import random
	pattern = '1234567890&!?#abcdefghijklmnopqrstuvwxyzABCDFGHYJKLMNOPQRSTUVWXYZ'
	key = ''
	for x in xrange(0,8):
		key += pattern[random.randrange(0,(len(pattern) - 1))]
	return '%s%s'%('SC',key)

@transaction.commit_manually
def ws_cotiza_proveedor(request):
	data = 'success'
	# Obteniendo el nro de Cotizacion
	cn = connection.cursor()
	cn.execute("SELECT DISTINCT nrocotizacion FROM almacen.sumcot WHERE nrosuministro LIKE '"+request.GET['nro']+"'")
	nrocot = cn.fetchone()
	cn.close()
	# Consultando Detalle de Suministro
	cn = connection.cursor()
	cn.execute("SELECT DISTINCT materialesid,SUM(cantidad) as cantidad FROM almacen.detsuministro WHERE nrosuministro LIKE '"+request.GET['nro']+"' AND materialesid IN "+request.GET['mat']+" GROUP BY materialesid ORDER BY materialesid ASC")
	ldet = cn.fetchall()
	cn.close()
	# Saved details cotizacion
	for x in ldet:
		cant = x[1]
		print cant
		cn = connection.cursor()
		cad = "INSERT INTO logistica.detcotizacion(nrocotizacion,rucproveedor,materialesid,cantidad) VALUES('"+nrocot[0]+"','"+request.GET['ruc']+"','"+x[0]+"',%d)"%(cant)
		cn.execute(cad)
		transaction.set_dirty()
		transaction.commit()
		cn.close()

	# Creando key para provaeedor
	# Obteniendo Auto Key Generado
	key = generateKey()
	cn = connection.cursor()
	cn.execute("INSERT INTO logistica.autogenerado(rucproveedor,nrocotizacion,keygen) VALUES('"+request.GET['ruc']+"','"+nrocot[0]+"','"+key+"')")
	transaction.set_dirty()
	transaction.commit()
	cn.close()

	return HttpResponse(data,mimetype='application/html')

@transaction.commit_manually
def ws_finalize_cotiza_sum(request):
	if request.method == 'GET':
		data = 'success'
		cn = connection.cursor()
		cn.execute("UPDATE almacen.suministro SET esid = '48' WHERE nrosuministro LIKE '"+request.GET['nro']+"'")
		transaction.set_dirty()
		transaction.commit()
		cn.close()

		return HttpResponse(data,mimetype='application/html')

"""
## Cotizacion 
"""
def ws_consulta_det_mat(request):
	if request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT matmed FROM admin.materiales WHERE matnom LIKE '"+request.GET['mat']+"'")
		lmed = cn.fetchall()
		cn.close()
		data = ''
		for x in lmed:
			data += "<option value='"+x[0]+"'>"+x[0]+"</option>"
		data +="|success"
		return HttpResponse(data,mimetype='application/html')

def ws_consulta_data_det(request):
	if request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT materialesid,matnom,matmed,matund FROM admin.materiales WHERE matnom LIKE '"+request.GET['mat']+"' AND matmed LIKE '"+request.GET['med']+"'")
		ldet = cn.fetchall()
		cn.close()
		data = ""
		for x in ldet:
			data += "<tr>"
			data += "<td>Codigo</td>"
			data += "<td id='matid'>"+x[0]+"</td>"
			data += "<td>Unidad</td>"
			data += "<td>"+x[3]+"</td>"
			data += "</tr>"
			data += "<tr>"
			data += "<td>Nombre</td>"
			data += "<td>"+x[1]+"</td>"
			data += "<td></td>"
			data += "<td></td>"
			data += "</tr>"
			data += "<tr>"
			data += "<td>Medida</td>"
			data += "<td>"+x[2]+"</td>"
			data += "<td></td>"
			data += "<td></td>"
			data += "</tr>"
		data += "|success"

		return HttpResponse(data,mimetype='application/html')

def ws_lista_detalle_cotiza(request):
	if request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT d.materialesid,m.matnom,m.matmed,m.matund,SUM(d.cantidad) as cantidad FROM logistica.tmpcotiza d INNER JOIN admin.materiales m ON d.materialesid LIKE m.materialesid WHERE d.empdni LIKE '"+request.GET['dni']+"' GROUP BY d.materialesid,m.matnom,m.matmed,m.matund")
		lmat = cn.fetchall()
		cn.close()
		data = ""
		i = 1
		for x in lmat:
			data += "<tr class='danger'>"
			data += "<td>"+str(i)+"</td>"
			data += "<td>"+x[0]+"</td>"
			data += "<td>"+x[1]+"</td>"
			data += "<td>"+x[2]+"</td>"
			data += "<td class='text-center'>"+x[3]+"</td>"
			data += "<td class='text-center'>"+str(x[4])+"</td>"
			data += "<td class='text-center'><button class='btn btn-xs tblack' onClick=editmattmp('"+x[0]+"');><span class='glyphicon glyphicon-edit'></span></button></td>"
			data += "<td class='text-center'><button class='btn btn-xs tblack' onClick=delmattmp('"+x[0]+"');><span class='glyphicon glyphicon-remove'></span></button></td>"
			data += "</tr>"
			i += 1

		return HttpResponse(data,mimetype='application/html')

@transaction.commit_manually
def ws_del_tmp_cotiza(request):
	if request.method == 'GET':
		data = 'success'
		cn = connection.cursor()
		cn.execute("DELETE FROM logistica.tmpcotiza WHERE empdni LIKE '"+request.GET['dni']+"'")
		transaction.set_dirty()
		transaction.commit()
		cn.close()
		return HttpResponse(data,mimetype='application/html')

@transaction.commit_manually
def ws_add_tmp_cotiza(request):
	if request.method == 'GET':
		data = 'success'
		cn = connection.cursor()
		sql = "INSERT INTO logistica.tmpcotiza VALUES('%s',%d,'%s')"%(request.GET['mat'],float(request.GET['cant']),request.GET['dni'])
		cn.execute(sql)
		#transaction.set_dirty()
		transaction.commit()
		cn.close()
		return HttpResponse(data,mimetype='application/html')

@transaction.commit_manually
def ws_del_mat_tmp_cotiza(request):
	if request.method == 'GET':
		data = 'success'
		cn = connection.cursor()
		cn.execute("DELETE FROM logistica.tmpcotiza WHERE empdni LIKE '"+request.GET['dni']+"' AND materialesid LIKE '"+request.GET['mat']+"'")
		transaction.commit()
		cn.close()
		return HttpResponse(data,mimetype="application/html")

@transaction.commit_manually
def ws_edit_mat_tmp_cotiza(request):
	if request.method == 'GET':
		cn = connection.cursor()
		cn.execute("DELETE FROM logistica.tmpcotiza WHERE empdni LIKE '"+request.GET['dni']+"' AND materialesid LIKE '"+request.GET['mat']+"'")
		transaction.commit()
		cn.close()
		data = 'success'
		cn = connection.cursor()
		sql = "INSERT INTO logistica.tmpcotiza VALUES('%s',%d,'%s')"%(request.GET['mat'],float(request.GET['cant']),request.GET['dni'])
		cn.execute(sql)
		transaction.commit()
		cn.close()
		return HttpResponse(data,mimetype="application/html")

@transaction.commit_manually
def ws_save_cotizacion_simple(request):
	if request.method == 'GET':
		data = 'success'
		# obteniendo nro de cotizacion
		cn = connection.cursor()
		cn.execute("SELECT * FROM logistica.spnuevacotizacion()")
		cot = cn.fetchone()
		cn.close()
		# guardando cotizacion
		#print cot[0]
		cn = connection.cursor()
		cn.execute("INSERT INTO logistica.cotizacion VALUES('"+cot[0].strip()+"','"+request.GET['dni']+"',now(),'"+request.GET['fec']+"'::date,'"+request.GET['obs']+"','14' )")
		transaction.set_dirty()
		transaction.commit()
		cn.close()
		data = str(cot[0].strip())
		return HttpResponse(data,mimetype='application/html')

def ws_list_tmp_cotiza(request):
	if request.method == 'GET':
		data = ''
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT d.materialesid,m.matnom,m.matmed,m.matund,SUM(d.cantidad) as cantidad FROM logistica.tmpcotiza d INNER JOIN admin.materiales m ON d.materialesid LIKE m.materialesid WHERE d.empdni LIKE '"+request.GET['dni']+"' GROUP BY d.materialesid,m.matnom,m.matmed,m.matund ")
		lista = cn.fetchall()
		i = 1
		for x in lista:
			data += "<tr class='warning'>"
			data += "<td>"+str(i)+"</td>"
			data += "<td>"+str(x[0])+"</td>"
			data += "<td>"+str(x[1])+"</td>"
			data += "<td>"+x[2]+"</td>"
			data += "<td>"+str(x[3])+"</td>"
			data += "<td>"+str(x[4])+"</td>"
			data += "<td><input type='checkbox' name='mats' value='"+str(x[0])+"' /></td>"
			data += "</tr>"
			i += 1

		return HttpResponse(data,mimetype='application/json')

@transaction.commit_manually
def ws_cotiza_proveedor_simple(request):
	data = 'success'
	# Consultando Detalle de Suministro
	cn = connection.cursor()
	sql = "SELECT DISTINCT materialesid,SUM(cantidad) as cantidad FROM logistica.tmpcotiza WHERE empdni LIKE '"+request.GET['dni']+"' AND materialesid IN "+request.GET['mat']+" GROUP BY materialesid ORDER BY materialesid ASC"
	cn.execute(sql)
	ltmp = cn.fetchall()
	cn.close()
	# Saved details cotizacion
	for x in ltmp:
		cant = x[1]
		#print cant
		cad = "INSERT INTO logistica.detcotizacion(nrocotizacion,rucproveedor,materialesid,cantidad) VALUES('"+request.GET['nco']+"','"+request.GET['ruc']+"','"+x[0]+"',%d)"%(cant)
		print cad
		cn = connection.cursor()
		cn.execute(cad)
		transaction.set_dirty()
		transaction.commit()
		cn.close()

	# Creando key para provaeedor
	# Obteniendo Auto Key Generado
	key = generateKey()
	cn = connection.cursor()
	cn.execute("INSERT INTO logistica.autogenerado(rucproveedor,nrocotizacion,keygen) VALUES('"+request.GET['ruc']+"','"+request.GET['nco']+"','"+key+"')")
	transaction.set_dirty()
	transaction.commit()
	cn.close()

	return HttpResponse(data,mimetype='application/html')

@transaction.commit_manually
def ws_finish_cotiza_proveedor_simple(request):
	if request.method == 'GET':
		data = 'success'
		cn = connection.cursor()
		cn.execute("DELETE FROM logistica.tmpcotiza WHERE empdni LIKE '"+request.GET['dni']+"'")
		transaction.commit()
		cn.close()
		return HttpResponse(data,mimetype='application/html')