from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.db import connection, transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
		request.session['access'] = 'success'
		return HttpResponseRedirect('http://190.41.246.91:8000/logistica/')
		#return render_to_response('logistica/home.html',context_instance=RequestContext(request))

"""
###
## 	Part Suministro
###
"""
def view_index(request):
	if str(request.session.get('access')) != 'success':
		return HttpResponseRedirect('http://190.41.246.91/web/')
	elif request.method == 'GET':
		tipo_cambio_sbs()
		#ctx = { 'dniicr': request.session['dni'], 'nomicr' : request.session['nom'], 'caricr':request.session['car'] }
		return render_to_response('logistica/home.html',context_instance=RequestContext(request))

def view_logout(request):
	#Session.objects.all().delete();
	del request.session['usericr']
	del	request.session['dniicr']
	del	request.session['nomicr']
	del	request.session['caricr']
	del request.session['access']
	return HttpResponseRedirect('http://190.41.246.91/web/')

def view_aprobarsuministro(request):
	if str(request.session.get('access')) != 'success':
		return HttpResponseRedirect('http://190.41.246.91/web/')
	elif request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT almacenid,descri FROM admin.almacenes")
		listal = dictfetchall(cn) #cn.fetchall()
		ctx = { 'listal':listal }
		return render_to_response('logistica/suministro.html',ctx,context_instance=RequestContext(request))

def view_cotiza_suministro(request):
	if str(request.session.get('access')) != 'success':
		return HttpResponseRedirect('http://190.41.246.91/web/')
	elif request.method == 'GET':
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
	if str(request.session.get('access')) != 'success':
		return HttpResponseRedirect('http://190.41.246.91/web/')
	elif request.method == 'GET':
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

def view_list_cotizacion(request):
	if str(request.session.get('access')) != 'success':
		return HttpResponseRedirect('http://190.41.246.91/web/')
	elif request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT c.nrocotizacion,c.fecha,c.fecreq,d.rucproveedor,s.razonsocial FROM "+
					"logistica.cotizacion c inner join logistica.detcotizacion d "+
					"ON c.nrocotizacion like d.nrocotizacion "+
					"INNER JOIN admin.proveedor s "+
					"ON d.rucproveedor like s.rucproveedor "+
					"WHERE c.estado like '14' "+
					"ORDER BY nrocotizacion ASC")
		lcot = dictfetchall(cn)
		cn.close()
		paginator = Paginator(lcot,8)
		try:
			page = request.GET['page']
		except Exception, e:
			page = ''
		try:
			cotizacion = paginator.page(page)
		except PageNotAnInteger:
			cotizacion = paginator.page(1)
		except EmptyPage:
			cotizacion = paginator.page(paginator.num_pages)

		#np = [ i+1 for i in xrange(cotizacion.paginator.num_pages)]
		ctx = { 'lcot' : cotizacion }
		return render_to_response('logistica/list_cotizacion.html',ctx,context_instance=RequestContext(request))

def view_compare_supplier(request,nro):
	if str(request.session.get('access')) != 'success':
		return HttpResponseRedirect('http://190.41.246.91/web/')
	elif request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT d.rucproveedor,p.razonsocial FROM logistica.detcotizacion d INNER JOIN admin.proveedor p "+
					"ON d.rucproveedor=p.rucproveedor "+
					"INNER JOIN logistica.cotizacion c "+
					"ON c.nrocotizacion LIKE d.nrocotizacion "+
					"WHERE d.nrocotizacion LIKE '"+nro+"' AND TRIM(c.estado) NOT LIKE '03' ORDER BY d.rucproveedor ASC")
		lsu = dictfetchall(cn)
		cn.close()
		cn = connection.cursor()
		cn.execute("SELECT monedaid,nomdes FROM admin.moneda")
		mo = dictfetchall(cn)
		cn.close()
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT documentoid,docnom FROM admin.documentos ORDER BY docnom ASC")
		doc = dictfetchall(cn)
		cn.close()
		cn = connection.cursor()
		cn.execute("SELECT DISTINCT pagoid,nompag FROM admin.fpago ORDER BY nompag ASC")
		pag = dictfetchall(cn)
		cn.close()
		ctx = { 'nro' : nro, 'lsu' : lsu, 'lmo' : mo, 'ldoc' : doc, 'lpag' : pag }
		return render_to_response('logistica/compare_supplier.html',ctx,context_instance=RequestContext(request))


@transaction.commit_on_success
def tipo_cambio_sbs():
	cn = connection.cursor()
	cn.execute("SELECT admin.spconsultatc()")
	vtc = cn.fetchone()
	cn.close()
	if vtc[0] != 'existe':
		#print vtc[0]
		from bs4 import BeautifulSoup
		from urllib2 import urlopen
		import urllib2
		# obteniedo datos
		url = "http://www.sbs.gob.pe/"
		proxy = urllib2.ProxyHandler( {'http': 'http://172.16.0.1:8080'} )
		# Create an URL opener utilizing proxy
		opener = urllib2.build_opener( proxy )
		urllib2.install_opener( opener )
		# Aquire data from URL
		request = urllib2.Request( url )
		response = urllib2.urlopen( request )
		html = response.read()
		soup = BeautifulSoup(html)
		current_compra = soup.find('p','WEB_compra').span.contents[0]
		current_venta = soup.find('p','WEB_venta').span.contents[0]
		current_compra = current_compra.strip()
		current_venta = current_venta.strip()
		current_compra = float(current_compra)
		current_venta = float(current_venta)
		# almacenando en la db
		try:
			cn = connection.cursor()
			sql = "SELECT * FROM admin.spgrabartipocambio('00002',%f,%f)"%(current_compra,current_venta)
			cn.execute(sql)
			transaction.commit()
			#res = cn.fetchone()
			cn.close()
		except Exception, e:
			transaction.rollback()
			raise e