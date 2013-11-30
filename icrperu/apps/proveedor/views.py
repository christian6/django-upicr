from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session
from django.db import connection

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
"""
####
## 	Request Date Login
####
"""
def view_logout_supliert(request):
	if request.method == 'GET':
		del request.session['rucpro']
		del request.session['rznpro']
		del request.session['tippro']
		del request.session['accesssupplier']
		return HttpResponseRedirect('/proveedor/')

def view_login_supplier(request):
	if request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT * FROM public.spvalidloginproveedor('"+request.GET['username']+"','"+request.GET['passwd']+"')")
		valid = cn.fetchone()
		data = valid[0]
		if len(data) == 11:
			cn = connection.cursor()
			cn.execute("SELECT rucproveedor,razonsocial,tipo FROM admin.proveedor WHERE rucproveedor LIKE '"+data+"'")
			lpro = cn.fetchall()
			for x in lpro:
				request.session['rucpro'] = x[0]
				request.session['rznpro'] = x[1]
				request.session['tippro'] = x[2]
				request.session['accesssupplier'] = 'success'

			data = 'success'
		
		return HttpResponse(data,mimetype='application/json')
"""
### Page First
"""
def view_index_supplier(request):
	#print request.session.get('accesssupplier')
	if str(request.session.get('accesssupplier')) == 'success':
		return HttpResponseRedirect('home/')
	elif request.method == 'GET':
		return render_to_response('proveedor/inicio.html',context_instance=RequestContext(request))

def view_home_supplier(request):
	if str(request.session.get('accesssupplier')) != 'success':
		return HttpResponseRedirect('/proveedor/')
	elif request.method == 'GET':
		return render_to_response('proveedor/home.html',context_instance=RequestContext(request))

def view_list_cotizaciones_supplier(request):
	if str(request.session.get('accesssupplier')) != 'success':
		return HttpResponseRedirect('/proveedor/')
	elif request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT c.nrocotizacion,c.fecha::date,c.fecreq::date FROM logistica.cotizacion c INNER JOIN logistica.detcotizacion d ON c.nrocotizacion LIKE d.nrocotizacion INNER JOIN logistica.cotizacioncli l ON c.nrocotizacion NOT LIKE l.nrocotizacion WHERE d.rucproveedor LIKE '"+request.session['rucpro']+"' AND TRIM(c.estado) LIKE '14' ORDER BY c.nrocotizacion DESC")
		lcot = dictfetchall(cn)
		cn.close()
		ctx = { 'lcot' : lcot }
		return render_to_response('proveedor/list_cotizacion.html',ctx,context_instance=RequestContext(request))

def view_cotizacion_supplier(request,nro):
	if str(request.session.get('accesssupplier')) != 'success':
		return HttpResponseRedirect('/proveedor/')
	elif request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT p.rucproveedor,p.razonsocial,p.direccion,a.paisnom,d.deparnom,r.provnom,i.distnom "+
					"FROM admin.proveedor p INNER JOIN admin.pais a "+
					"ON p.paisid=a.paisid "+
					"INNER JOIN admin.departamento d "+
					"ON p.departamentoid=d.departamentoid "+
					"INNER JOIN admin.provincia r "+
					"ON p.provinciaid=r.provinciaid "+
					"INNER JOIN admin.distrito i "+
					"ON p.distritoid=i.distritoid "+
					"WHERE a.paisid LIKE d.paisid AND d.departamentoid LIKE r.departamentoid "+
					"AND r.provinciaid LIKE i.provinciaid AND p.rucproveedor LIKE '"+str(request.session.get('rucpro'))+"' LIMIT 1 OFFSET 0")
		det = dictfetchall(cn)
		cn.close()
		cn = connection.cursor()
		cn.execute("SELECT * FROM logistica.spconsultardetcotizacion('"+nro+"','"+request.session.get('rucpro')+"')")
		ldet = dictfetchall(cn)
		cn.close()
		cn = connection.cursor()
		cn.execute("SELECT monedaid, nomdes FROM admin.moneda WHERE esid LIKE '10'")
		lmo = dictfetchall(cn)
		cn.close()
		ctx = { 'nro' : nro, 'det' : det, 'ldet' : ldet, 'lmo' : lmo }
		return render_to_response('proveedor/view_cotizacion.html',ctx,context_instance=RequestContext(request))

def view_list_Order_buy(request):
	if str(request.session.get('accesssupplier')) != 'success':
		return HttpResponseRedirect('/proveedor/')
	elif request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT c.nrocompra,m.nomdes,e.empnom||', '||e.empape as nombre,c.fecha,c.fecent,s.esnom FROM logistica.compras c INNER JOIN admin.empleados e "+
							"ON c.empdni = e.empdni INNER JOIN admin.moneda m ON c.monedaid=m.monedaid INNER JOIN admin.estadoes s ON c.esid = s.esid "+
							"WHERE c.rucproveedor LIKE '"+request.session.get('rucpro')+"' AND c.esid LIKE '12'")
		lbuy = dictfetchall(cn)
		cn.close()
		ctx = { 'lbuy' : lbuy }
		return render_to_response('proveedor/list_buy.html',ctx,context_instance=RequestContext(request))