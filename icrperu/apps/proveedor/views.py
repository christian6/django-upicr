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

def view_securitylog(request):
	if request.method == 'GET':
		cn = connection.cursor()
		cn.execute("SELECT * FROM public.spvalidloginproveedor('"+request.GET['username']+"','"+request.GET['passwd']+"')")
		valid = cn.fetchone()
		data = valid[0]
		if len(data) == 11:
			cn = connection.cursor()
			cn.execute("SELECT rucproveedor,razonsocial,tipo FROM admin.proveedor WHERE rucproveedor LIKE '"+data+"'")
			lpro = dictfetchall(cn)
			for x in lpro:
				request.session['rucpro'] = x['rucproveedor']
				request.session['rznpro'] = x['razonsocial']
				request.session['tippro'] = x['tipo']
				request.session['access'] = 'success'
			data = 'success'
		
		return HttpResponse(data,mimetype='application/json')

"""
### Page First
"""
def view_index(request):
	print request.session.get('access')
	if str(request.session.get('access')) == 'success':
		return HttpResponseRedirect('home/')
	if request.method == 'GET':
		return render_to_response('proveedor/inicio.html',context_instance=RequestContext(request))

def view_home(request):
	print request.session.get('access')
	if str(request.session.get('access')) != 'success':
		return HttpResponseRedirect('/proveedor/')
	if request.method == 'GET':
		return render_to_response('proveedor/home.html',context_instance=RequestContext(request))