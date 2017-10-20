from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .forms import registroAdmin, registroEgresado
from django.contrib.auth.decorators import login_required

def registro(request, type):
	context = {
		'type': type,
	}
	if(type=="admin"):
		form = registroAdmin()
		context['form'] = form
	else:
		form = registroEgresado()
		context['form'] = form

	if(request.POST):
		pass
	else:
		return render(request,'usuarios/registro.html', context)



@login_required
def Bienvenido(request):	
	return render_to_response('bienvenido.html',{})


def index(request):
    return render(request, 'index/index.html', {})