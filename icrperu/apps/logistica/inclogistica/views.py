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
				data += "<td>"+str(x[1])+"</td>"
				data += "<td>"+str(x[2])+"</td>"
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
			data += "<td>"+str(x[2])+"</td>"
			data += "<td>"+str(x[3])+"</td>"
			data += "<td>"+str(x[4])+"</td>"
			data += "<td><input type='checkbox' name='mat' id='"+str(x[0])+"' /></td>"
			data += "</tr>"
			i += 1

		return HttpResponse(data,mimetype='application/json')