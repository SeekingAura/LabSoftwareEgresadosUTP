from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader


from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.validators import EmailValidator, ValidationError
from django.contrib import messages

from usuarioAdminEgresado.models import UsuariosAdminEgresado
from usuarioAdministrador.models import UsuarioAdministrador
from usuarioEgresado.models import UsuarioEgresado
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import password_validators_help_text_html
from .forms import primerLogin_Form, departamentoValidator
from .decorators import *


		
@login_required(login_url="usuario:login")
@primerLogin(index_url="usuarioEgre:primerLogin")
@redirectEgresado(index_url="usuarioAdmin:index")
def index_view(request):
	username = None
	context={'username': username, 'tipoUser' : "Egresado", 'user' : request.user}
	if request.user.is_authenticated():
		username = request.user.first_name
		context['username']=username
		
	return render(request, 'egresado/index.html',context)

@login_required(login_url="usuario:login")
@primerLogin(index_url="usuarioEgre:index", isNotYet=False)
@redirectEgresado(index_url="usuarioAdmin:index")
def primerLogin_view(request):
	context={}
	form=primerLogin_Form()
	context['form'] = form
	if(request.method == 'POST'):
		form=primerLogin_Form(data=request.POST)
		context['form'] = form
		for key, value in request.POST.items():
			print(key, value)
		#print("es publico?",request.POST.get("isPublico"))#get on or none
		#print("intereses", request.POST.getlist("intereses"))
		#print("se hizo un post")
		valido=True
		if(not departamentoValidator(request.POST.get("pais"), request.POST.get("departamento"))):
			messages.error(request, 'El departamento dado no corresponde al pais seleccionado')
			valido=False
		if(len(request.POST.getlist("intereses"))==0):
			messages.error(request, 'Debe tener seleccionado al menos 1 interes')
			valido=False
		#1997 2002 fechaNacimiento_year, fechaNacimiento_month, fechaNacimiento_day
		if(int(request.POST.get("fechaNacimiento_year"))>=int(request.POST.get("graduacion"))-15):
			messages.error(request, 'La fecha de graduación no es acorde a la de su nacimiento')
			valido=False
		if(form.is_valid() and valido):
			
			
			
			messages.success(request, 'es valido')
			print("es valido!")
		else:
			messages.error(request, 'Hay errores en el registro, revise los campos')
	return render(request, 'egresado/primerlogin.html',context)