from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
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
def view_securitylog(request):
	if request.method == 'GET':
		request.session['usericr'] = request.GET['usr']
		request.session['dniicr'] = request.GET['dni']
		request.session['nomicr'] = request.GET['nom']
		request.session['caricr'] = request.GET['cargo']
		return HttpResponseRedirect('http://190.41.246.91:8000/logistica/')
		#return render_to_response('logistica/home.html',context_instance=RequestContext(request))

"""
###
## 	Part Suministro
###
"""
def view_index(request):
	#ctx = { 'dniicr': request.session['dni'], 'nomicr' : request.session['nom'], 'caricr':request.session['car'] }
	return render_to_response('logistica/home.html',context_instance=RequestContext(request))

def view_logout(request):
	Session.objects.all().delete();
	return HttpResponseRedirect('http://190.41.246.91/web/')

def view_aprobarsuministro(request):
	cn = connection.cursor()
	cn.execute("SELECT almacenid,descri FROM admin.almacenes")
	listal = dictfetchall(cn) #cn.fetchall()
	ctx = { 'listal':listal }
	return render_to_response('logistica/suministro.html',ctx,context_instance=RequestContext(request))

def view_cotiza_suministro(request):
	if request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT s.nrosuministro,a.descri,e.empnom||', '||e.empape as empn, s.fecha::date,s.fecreq::date FROM almacen.suministro s INNER JOIN admin.almacenes a ON s.almacenid=a.almacenid INNER JOIN admin.empleados e ON s.empdni=e.empdni WHERE s.esid LIKE '38'")
		lista = dictfetchall(cn)
		cn.close()
		cn = connection.cursor()
		cn.execute("SELECT rucproveedor,razonsocial FROM admin.proveedor WHERE esid LIKE '15' ORDER BY razonsocial ASC")
		listp = dictfetchall(cn)
		cn.close()
		ctx = { 'lista':lista, 'listp':listp }
		return render_to_response('logistica/cotizasuministro.html',ctx,context_instance=RequestContext(request))
"""
###
## 	Part Cotizacion
###
"""
def view_cotizacion_simple(request):
	cn =  connection.cursor()
	cn.execute("SELECT DISTINCT matnom FROM admin.materiales ORDER BY matnom ASC")
	lmat = dictfetchall(cn)
	cn.close()
	cn = connection.cursor()
	cn.execute("SELECT DISTINCT rucproveedor,razonsocial FROM admin.proveedor WHERE esid LIKE '15' ORDER BY razonsocial ASC")
	lpro = dictfetchall(cn)
	cn.close()
	ctx = { 'lmat':lmat, 'lpro': lpro }
	return render_to_response('logistica/cotizacion_simple.html',ctx,context_instance=RequestContext(request))