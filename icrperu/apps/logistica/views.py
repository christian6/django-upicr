from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
#from django.contrib.session import session

def view_index(request):
	ctx = { 'dni': request.session['dni'] }
	return render_to_response('logistica/home.html',ctx,context_instance=RequestContext(request))

def view_securitylog(request,dni,nombre,cargo):
	request.session['dni'] = dni
	request.session['nom'] = nombre
	request.session['car'] = cargo
	return HttpResponseRedirect('http://190.41.246.91:8000/logistica/')