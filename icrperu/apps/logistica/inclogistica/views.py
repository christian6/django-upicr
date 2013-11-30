#!-*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.db import connection, transaction
#from django.core import serializers
from django.utils import simplejson

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
	pattern = '1234567890!#abcdefghijklmnopqrstuvwxyzABCDFGHYJKLMNOPQRSTUVWXYZ'
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

	# Creando key para proveedor
	# Obteniendo Auto Key Generado
	key = generateKey()
	cn = connection.cursor()
	cn.execute("INSERT INTO logistica.autogenerado(rucproveedor,nrocotizacion,keygen) VALUES('"+request.GET['ruc']+"','"+nrocot[0]+"','"+key+"')")
	transaction.set_dirty()
	transaction.commit()
	cn.close()

	## Enviado Email a Proveedor
	
	

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
		cn.close()
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

def ws_compare_supplier(request):
	if request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT nrocotizacion,rucproveedor FROM logistica.detcotizacion WHERE nrocotizacion LIKE '"+request.GET.get('nro')+"' ORDER BY rucproveedor ASC")
		lsupplier = dictfetchall(cn)
		cn.close()

		cn = connection.cursor()
		cn.execute("SELECT DISTINCT d.materialesid,m.matnom,m.matmed,m.matund,d.cantidad FROM logistica.detcotizacion d INNER JOIN admin.materiales m "+
					"ON d.materialesid LIKE m.materialesid "+
					"where d.nrocotizacion like '"+request.GET.get('nro')+"'")
		ldet = dictfetchall(cn)
		cn.close()
		data = ''
		i = 0
		for x in ldet:
			i+=1
			data += '<tr>'
			data += '<td><input type="checkbox" name="mat" value="'+x['materialesid']+'"></td>'
			data += '<td>'+str(i)+'</td>'
			data += '<td>'+x['materialesid']+'</td>'
			data += '<td>'+x['matnom']+'</td>'
			data += '<td>'+x['matmed']+'</td>'
			data += '<td>'+x['matund']+'</td>'
			data += '<td id="c'+x['materialesid']+'">'+str(x['cantidad'])+'</td>'
			for s in lsupplier:
				cn = connection.cursor()
				cn.execute("SELECT DISTINCT materialesid,precio,marca FROM logistica.detcotizacion WHERE nrocotizacion LIKE '"+request.GET.get('nro')+"' AND rucproveedor LIKE '"+s['rucproveedor']+"' AND materialesid LIKE '"+x['materialesid']+"' ")
				det = dictfetchall(cn)
				cn.close()
				for p in det:
					data += '<td class="text-right" id="op'+s['rucproveedor']+str(x['materialesid'])+'">'+str(p['precio'])+'</td>'
					data += '<td><input type="number"  class="form-control input-xs text-right" value="'+str(p['precio'])+'" id="'+s['rucproveedor']+p['materialesid']+'"></td>'
					data += '<td>'+p['marca']+'</td>'
			
		return HttpResponse(data,mimetype='application/html')

def ws_obtener_money_supplier(request):
	if request.method == 'GET':
		data = '{ "status": "Nothing" }'
		try:
			cn = connection.cursor()
			cn.execute("SELECT m.nomdes FROM logistica.cotizacioncli c INNER JOIN admin.moneda m ON c.monedaid LIKE m.monedaid WHERE c.nrocotizacion LIKE '"+request.GET.get('nro')+"' AND c.rucproveedor LIKE '"+request.GET.get('ruc')+"'")
			mo = cn.fetchone()
			cn.close()
			if mo[0] != '':
				data = '{ "status": "success", "money" : "'+mo[0]+'" }'
			else:
				data = '{ "status": "Nothing" }'
		except Exception, e:
			data = '{ "status": "Nothing" }'

		data = simplejson.dumps(data)
		return HttpResponse(data, mimetype='application/json')

def ws_obtener_det_mat_buy(request):
	if request.method == 'GET':
		con ='"contacto" : "Nothing"'
		sts = '"status" : "fail"'
		try:
			mats = request.GET.get('mat')
			cn =  connection.cursor()
			cn.execute("SELECT materialesid,matnom,matmed,matund FROM admin.materiales WHERE materialesid IN ("+mats+")")
			lmat = dictfetchall(cn)
			cn.close()
			sts = '"status" : "success"'
		except Exception, e:
			sts = '"status" : "fail"'
		try:
			cn = connection.cursor()
			cn.execute("SELECT contacto FROM logistica.cotizacioncli WHERE nrocotizacion LIKE '"+request.GET.get('nro')+"' AND rucproveedor LIKE '"+request.GET.get('ruc')+"' ")
			lcon = cn.fetchone()
			cn.close()
			sts = '"status" : "success"'
			con ='"contacto" : "'+str(lcon[0])+'"'
		except Exception, e:
			pass
		
		lmat = simplejson.dumps(lmat)
		data = '{"mat" : '+str(lmat)+', '+sts+', '+con+' }'
		return HttpResponse(data, mimetype='application/json')

def ws_type_change_money(request):
	if request.method == 'GET':
		data = {}
		sts = ''
		try:
			cn = connection.cursor()
			cn.execute("SELECT tcompra,tventa FROM admin.tipocambio WHERE monedaid LIKE '00002' AND fecha::date = now()::date LIMIT 1 OFFSET 0")
			lchange = dictfetchall(cn)
			cn.close()
			sts = 'success'
		except Exception, e:
			lchange = 'Nothing'
			sts = 'fail'
			raise e
		data["status"] = sts
		data['tc'] = lchange
		data = simplejson.dumps(data)
		return HttpResponse(data, mimetype='application/json')

@transaction.autocommit
def ws_save_order_buy(request):
	prm = request.GET.get('prm')
	#data = simplejson.dumps(data)
	data = simplejson.loads(prm)
	da = {}
	# Obteniendo Codigo de Orden de Compra
	cn = connection.cursor()
	cn.execute("SELECT logistica.spnewcompra()")
	ncod = cn.fetchone()
	cn.close()
	
	try:
		#Generando Orden de Compra
		cn = connection.cursor()
		cn.execute("INSERT INTO logistica.compras(nrocompra,rucproveedor,empdni,nrocotizacion,lugent,documentoid,pagoid,monedaid,fecent,contacto,esid) VALUES('"+ncod[0]+"','"+data['ruc']+"','"+request.session.get('dniicr')+"','"+data['ncot']+"','"+data['lug']+"','"+data['doc']+"','"+data['pag']+"','"+data['mid']+"','"+data['ent']+"'::date,'"+data['cont']+"','12')")
		transaction.set_dirty()
		transaction.commit()
		cn.close()

		for x in xrange(0,len(data['mat'])):
			#da += str(data['mat'][x][0])+"', "+str(data['mat'][x][1])+", "+str(data['mat'][x][2])+'<br>'
			cn = connection.cursor()
			cn.execute("INSERT INTO logistica.detcompras(nrocompra,materialesid,cantidad,precio,cantstatic,flag) VALUES ('"+ncod[0]+"', '"+str(data['mat'][x][0])+"', "+str(data['mat'][x][1])+", "+str(data['mat'][x][2])+", "+str(data['mat'][x][1])+", '0')")
			#transaction.set_dirty()
			transaction.commit()
			cn.close()
			#da += str(data['mat'][x])+ ' > len '+str(len(data['mat'][x]))	

		da['status'] = 'success'
		da['nro'] = ncod[0]
		da['ruc'] = data['ruc']
	except Exception, e:
		da['status'] = 'fail'

	da = simplejson.dumps(da)
	return HttpResponse(da, mimetype='application/json')

@transaction.autocommit
def wv_change_status_cotizacion(request):
	if request.method == 'GET':
		data = {}
		cn = connection.cursor()
		cn.execute("UPDATE logistica.cotizacion SET estado = '03' WHERE nrocotizacion LIKE '"+request.GET.get('nro')+"'")
		transaction.commit()
		cn.close()
		data['status'] = 'success'
		data = simplejson.dumps(data)
		return HttpResponse(data,mimetype='application/json')

def wv_search_key_cotizacion(request):
	if request.method == 'GET':
		query = "SELECT DISTINCT a.nrocotizacion,a.rucproveedor,p.razonsocial,a.keygen,c.fecha::date::varchar FROM logistica.autogenerado a INNER JOIN logistica.cotizacion c ON a.nrocotizacion = c.nrocotizacion INNER JOIN admin.proveedor p ON a.rucproveedor = p.rucproveedor WHERE c.estado LIKE '14' "
		if request.GET.get('type') == 'nro':
			query = '%s %s %s'%(query," AND c.nrocotizacion LIKE '"+request.GET.get('nro')+"' ","ORDER BY c.nrocotizacion DESC")
		elif request.GET.get('type') != 'nro':
			if request.GET.get('type') == 'one':
				query = '%s %s %s'%(query," AND c.fecha::date = '"+request.GET.get('fi')+"'::date ","ORDER BY c.nrocotizacion DESC")
			elif request.GET.get('type') == 'plus':
				query = '%s %s %s'%(query," AND c.fecha::date BETWEEN '"+request.GET.get('fi')+"' AND '"+request.GET.get('ff')+"' ","ORDER BY c.nrocotizacion DESC")
		da  = {}
		try:
			cn = connection.cursor()
			cn.execute(query)
			ldet = dictfetchall(cn)
			cn.close()
			da['status'] = 'success'
		except Exception, e:
			raise e
			da['status'] = 'fail'
		da['list'] = ldet
		data = simplejson.dumps(da)
		return HttpResponse(data,mimetype='application/json')

def ws_search_departamento(request):
	if request.method == 'GET':
		da = {}
		try:
			cn = connection.cursor()
			cn.execute("SELECT departamentoid,deparnom FROM admin.departamento WHERE paisid LIKE '"+request.GET.get('pais')+"'")
			ld = dictfetchall(cn)
			cn.close()
			da['status'] = 'success'
			da['ldet'] = ld
		except Exception, e:
			raise e
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data,mimetype='application/json')

def ws_search_provincia(request):
	if request.method == 'GET':
		da = {}
		try:
			cn = connection.cursor()
			cn.execute("SELECT provinciaid,provnom FROM admin.provincia WHERE paisid LIKE '"+request.GET.get('pais')+"' AND departamentoid LIKE '"+request.GET.get('dep')+"'")
			ld = dictfetchall(cn)
			cn.close()
			da['status'] = 'success'
			da['ldet'] = ld
		except Exception, e:
			raise e
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data,mimetype='application/json')

def ws_search_distrito(request):
	if request.method == 'GET':
		da = {}
		try:
			cn = connection.cursor()
			cn.execute("SELECT distritoid,distnom FROM admin.distrito WHERE paisid LIKE '"+request.GET.get('pais')+"' AND departamentoid LIKE '"+request.GET.get('dep')+"' AND provinciaid LIKE '"+request.GET.get('pro')+"'")
			ld = dictfetchall(cn)
			cn.close()
			da['status'] = 'success'
			da['ldet'] = ld
		except Exception, e:
			raise e
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data,mimetype='application/json')

@transaction.commit_manually
def ws_save_supplier(request):
	if request.method == 'GET':
		da = {}
		try:
			cn = connection.cursor()
			cn.execute("SELECT COUNT(*) FROM admin.proveedor WHERE rucproveedor LIKE '"+request.GET.get('ruc')+"' ")
			nt = cn.fetchone()
			cn.close()
			if nt[0] > 0:
				cn = connection.cursor()
				cn.execute("UPDATE admin.proveedor SET razonsocial='"+request.GET.get('rs')+"',direccion = '"+request.GET.get('dir')+"',paisid = '"+request.GET.get('pais')+"',departamentoid='"+request.GET.get('dep')+"',provinciaid='"+request.GET.get('pro')+"',distritoid='"+request.GET.get('dist')+"',telefono='"+request.GET.get('tel')+"',tipo='"+request.GET.get('tipo')+"',origen='"+request.GET.get('ori')+"',esid='15', email='"+request.GET.get('mail')+"' WHERE rucproveedor LIKE '"+request.GET.get('ruc')+"'")
				transaction.set_dirty()
				transaction.commit()
				cn.close()
			else:
				cn = connection.cursor()
				cn.execute("INSERT INTO admin.proveedor VALUES('"+request.GET.get('ruc')+"','"+request.GET.get('rs')+"','"+request.GET.get('dir')+"','"+request.GET.get('paisid')+"','"+request.GET.get('dep')+"','"+request.GET.get('pro')+"','"+request.GET.get('dist')+"','"+request.GET.get('tel')+"','"+request.GET.get('tipo')+"','"+request.GET.get('ori')+"','15','"+request.GET.get('mail')+"')")
				transaction.set_dirty()
				transaction.commit()
				cn.close()
			da['status'] = 'success'
		except Exception, e:
			transaction.rollback()
			raise e
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data,mimetype='application/json')

@transaction.commit_manually
def ws_delete_supplier(request):
	if request.method == 'GET':
		da = {}
		try:
			cn = connection.cursor()
			cn.execute("UPDATE admin.proveedor SET esid = '16' WHERE rucproveedor LIKE '"+request.GET.get('ruc')+"'")
			transaction.set_dirty()
			transaction.commit()
			cn.close()
			da['status'] = 'success'
		except Exception, e: 
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data,mimetype='application/json')

@transaction.autocommit
def ws_saved_login_supplier(request):
	if request.method == 'GET':
		da = {}
		try:
			cn =  connection.cursor()
			cn.execute("SELECT COUNT(*) FROM public.loginpro WHERE rucproveedor LIKE '"+request.GET.get('ruc')+"'")
			log = cn.fetchone()
			cn.close()
			if log[0] > 0:
				cn = connection.cursor()
				cn.execute("UPDATE public.loginpro SET username = '"+request.GET.get('ruc')+"', passwd = '"+request.GET.get('passwd')+"' WHERE rucproveedor LIKE '"+request.GET.get('ruc')+"' ")
				transaction.commit()
				cn.close()
			else:
				cn = connection.cursor()
				cn.execute("INSERT INTO public.loginpro VALUES('"+request.GET.get('ruc')+"','"+request.GET.get('ruc')+"','"+request.GET.get('passwd')+"')")
				transaction.commit()
				cn.close()
			da['status'] = 'success'
		except Exception, e:
			transaction.rollback()
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data,mimetype='application/json')

@transaction.autocommit
def ws_upload_reade_cotizacion_simple(request):
	if request.method == 'POST':
		import os
		from django.conf import settings
		## Upload file xls 
		path = settings.PATH_PROJECT
		cot = 'media/store/templates/cotizacion/'
		pathabs = os.path.join(path,cot)
		if not os.path.exists(pathabs):
			os.makedirs(pathabs,0777)
			os.chmod(pathabs,0777)

		f = request.FILES['archivo']
		pathabs+='tmpcot.xls'
		destination = open(pathabs, 'wb+')
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close()
		os.chmod(pathabs,0777);
		### Ready file Xls
		import xlrd
		da = {}
		try:
			# declaramos un libro
			book = xlrd.open_workbook(pathabs,encoding_override='utf-8')
			## obtenemos las hojas existentes
			#sheets = book.sheet_name()
			# seleccionamos la hoja que vamos a trabajar
			sheet = book.sheet_by_index(0);
			## Obtener datos de la hoja
			for x in range(2,sheet.nrows):
				# obteniendo codigo de material y cantidad
				matid = sheet.cell(x,1)
				cant = sheet.cell(x,5)
				## accediendo a la base de datos y guardando los datos obtenidos
				cn = connection.cursor()
				print int(matid.value)
				cn.execute("INSERT INTO logistica.tmpcotiza VALUES('"+str(int(matid.value))+"',"+str(cant.value)+",'"+request.session.get('dniicr')+"')")
				transaction.commit()
				cn.close()
			da['status'] = 'success'
			os.remove(pathabs)
		except Exception, e:
			transaction.rollback()
			da['status'] = 'fail'
		
		data = simplejson.dumps(da)
		return HttpResponse(data, mimetype='application/json')

def ws_list_tmp_compra(request):
	if request.method == 'GET':
		da = {}
		try:
			cn = connection.cursor()
			cn.execute("SELECT DISTINCT d.materialesid,m.matnom,m.matmed,m.matund,SUM(d.cantidad) as cantidad,precio FROM logistica.tmpcompra d INNER JOIN admin.materiales m ON d.materialesid LIKE m.materialesid WHERE d.empdni LIKE '"+request.GET['dni']+"' GROUP BY d.materialesid,m.matnom,m.matmed,m.matund,precio ")
			lista = dictfetchall(cn)
			cn.close()
			da['status'] = 'success'
			da['list'] = lista
		except Exception, e:
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data, mimetype='application/json')

@transaction.commit_manually
def ws_delete_tmp_det_buy(request):
	if request.method == 'GET':
		da = {}
		try:
			cn = connection.cursor()
			cn.execute("DELETE FROM logistica.tmpcompra WHERE empdni LIKE '"+request.session.get('dniicr')+"'")
			transaction.set_dirty()
			transaction.commit()
			cn.close()
			da['status'] = 'success'
		except Exception, e:
			transaction.rollback()
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data, mimetype='application/json')

@transaction.commit_manually
def ws_add_tmp_detils_buy(request):
	if request.method == 'GET':
		da = {}
		try:
			cn = connection.cursor()
			sql = "INSERT INTO logistica.tmpcompra VALUES('%s',%d,%f,'%s')"%(request.GET['mat'],float(request.GET['cant']),float(request.GET['pre']),request.GET['dni'])
			cn.execute(sql)
			transaction.set_dirty()
			transaction.commit()
			cn.close()
			da['status'] = 'success'
		except Exception, e:
			transaction.rollback()
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data,mimetype='application/json')

@transaction.commit_manually
def ws_edit_mat_tmp_buy(request):
	if request.method == 'GET':
		da = {}
		try:
			cn = connection.cursor()
			cn.execute("DELETE FROM logistica.tmpcompra WHERE empdni LIKE '"+request.GET['dni']+"' AND materialesid LIKE '"+request.GET['mat']+"'")
			transaction.commit()
			cn.close()
			cn = connection.cursor()
			sql = "INSERT INTO logistica.tmpcompra VALUES('%s',%d,%f,'%s')"%(request.GET['mat'],float(request.GET['cant']),float(request.GET.get('pre')),request.GET['dni'])
			cn.execute(sql)
			transaction.commit()
			cn.close()
			da['status'] = 'success'
		except Exception, e:
			transaction.rollback()
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data,mimetype="application/json")

@transaction.commit_manually
def ws_delete_mat_tmp_buy(request):
	if request.method == 'GET':
		da = {}
		try:
			cn = connection.cursor()
			cn.execute("DELETE FROM logistica.tmpcompra WHERE materialesid LIKE '"+request.GET.get('mat')+"' AND empdni LIKE '"+request.GET.get('dni')+"'")
			transaction.set_dirty()
			transaction.commit()
			cn.close()
			da['status'] = 'success'
		except Exception, e:
			transaction.rollback()
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data, mimetype='application/json')

@transaction.commit_manually
def ws_save_mat_tmp_buy(request):
	pass

@transaction.autocommit
def ws_upload_ready_buy_tmp(request):
	if request.method == 'POST':
		import os
		from django.conf import settings
		## Upload file xls 
		path = settings.PATH_PROJECT
		com = 'media/store/templates/compras/'
		pathabs = os.path.join(path,com)
		if not os.path.exists(pathabs):
			os.makedirs(pathabs,0777)
			os.chmod(pathabs,0777)

		f = request.FILES['archivo']
		pathabs += 'tmpbuy.xls'
		destination = open(pathabs, 'wb+')
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close()
		os.chmod(pathabs,0777);
		### Ready file Xls
		import xlrd
		da = {}
		try:
			# declaramos un libro
			book = xlrd.open_workbook(pathabs,encoding_override='utf-8')
			## obtenemos las hojas existentes
			#sheets = book.sheet_name()
			# seleccionamos la hoja que vamos a trabajar
			sheet = book.sheet_by_index(0);
			## Obtener datos de la hoja
			for x in range(2,sheet.nrows):
				# obteniendo codigo de material y cantidad
				matid = sheet.cell(x,1)
				cant = sheet.cell(x,5)
				pre = sheet.cell(x,6)
				## accediendo a la base de datos y guardando los datos obtenidos
				cn = connection.cursor()
				cn.execute("INSERT INTO logistica.tmpcompra VALUES('"+str(int(matid.value))+"',"+str(cant.value)+","+str(pre.value)+",'"+request.session.get('dniicr')+"')")
				transaction.commit()
				cn.close()
			da['status'] = 'success'
			os.remove(pathabs)
		except Exception, e:
			transaction.rollback()
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data, mimetype='application/json')

@transaction.autocommit
def ws_saved_order_buy_single(request):
	if request.method == 'POST':
		#da = request.POST.get('lmat')
		prm = request.POST.get('lmat')
		#data = simplejson.dumps(data)
		data = simplejson.loads(prm)
		da = {}
		# Obteniendo Codigo de Orden de Compra
		cn = connection.cursor()
		cn.execute("SELECT logistica.spnewcompra()")
		ncod = cn.fetchone()
		cn.close()
		
		try:
			#Generando Orden de Compra
			cn = connection.cursor()
			cn.execute("INSERT INTO logistica.compras(nrocompra,rucproveedor,empdni,nrocotizacion,lugent,documentoid,pagoid,monedaid,fecent,contacto,esid) VALUES('"+ncod[0]+"','"+request.POST.get('pro')+"','"+request.session.get('dniicr')+"','','"+request.POST.get('lug')+"','"+request.POST.get('doc')+"','"+request.POST.get('pag')+"','"+request.POST.get('mo')+"','"+request.POST.get('fec')+"'::date,'"+request.POST.get('cont')+"','12')")
			transaction.set_dirty()
			transaction.commit()
			cn.close()

			for x in xrange(0,len(data['mat'])):
				#da += str(data['mat'][x][0])+"', "+str(data['mat'][x][1])+", "+str(data['mat'][x][2])+'<br>'
				cn = connection.cursor()
				cn.execute("INSERT INTO logistica.detcompras(nrocompra,materialesid,cantidad,precio,cantstatic,flag) VALUES ('"+ncod[0]+"', '"+str(data['mat'][x][0])+"', "+str(data['mat'][x][1])+", "+str(data['mat'][x][2])+", "+str(data['mat'][x][1])+", '0')")
				#transaction.set_dirty()
				transaction.commit()
				cn.close()
				#da += str(data['mat'][x])+ ' > len '+str(len(data['mat'][x]))
			
			cn = connection.cursor()
			cn.execute("DELETE FROM logistica.tmpcompra WHERE empdni LIKE '"+request.session.get('dniicr')+"'")
			transaction.set_dirty()
			transaction.commit()
			cn.close()

			da['status'] = 'success'
			da['nro'] = ncod[0]
		except Exception, e:
			da['status'] = 'fail'

		da = simplejson.dumps(da)
		return HttpResponse(da, mimetype='application/json')

def ws_consulting_order_buy(request):
	if request.method == 'GET':
		da = {}
		try:
			whe = ""
			if request.GET.get('tipo') == 'nro':
				whe = "c.nrocompra LIKE '"+request.GET.get('nro')+"' AND "
			elif request.GET.get('tipo') == 'one':
				whe = "c.fecha::date = '"+request.GET.get('fi')+"'::date AND "
			elif request.GET.get('tipo') == 'multi':
				whe = "c.fecha::date BETWEEN '"+request.GET.get('fi')+"'::date AND '"+request.GET.get('ff')+"'::date AND"

			sql = "SELECT c.nrocompra,c.rucproveedor,p.razonsocial,d.docnom,m.nomdes FROM logistica.compras c INNER JOIN admin.proveedor p ON c.rucproveedor LIKE p.rucproveedor INNER JOIN admin.documentos d ON c.documentoid LIKE d.documentoid INNER JOIN admin.moneda m ON c.monedaid LIKE m.monedaid WHERE %s c.esid LIKE '12'"%(whe)
			cn = connection.cursor()
			cn.execute(sql)
			lbuy = dictfetchall(cn)
			cn.close()
			da['status'] = 'success'
			da['lbuy'] = lbuy
		except Exception, e:
			da['status'] = 'fail'
		data = simplejson.dumps(da)
		return HttpResponse(data, mimetype='application/json')