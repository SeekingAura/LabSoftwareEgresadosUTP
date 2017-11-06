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
from usuarioAdministrador.models import UsuarioAdministrador, intereses
from usuarioEgresado.models import UsuarioEgresado, InteresesEgresado
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
			user=User.objects.get(username=request.user)
			userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
			userEgre=UsuarioEgresado.objects.get(userAdminEgre_id=userAdminEgre.DNI)
			
			userAdminEgre.pais=request.POST.get("pais")
			userAdminEgre.departamento=request.POST.get("departamento")
			
			for i in request.POST.getlist("intereses"):
				interes=intereses.objects.get(titulo=i)
				interes=InteresesEgresado.objects.create(userEgre=userEgre, interes=interes)
				interes.save()
			
			userEgre.fechaNacimiento=str(request.POST.get("fechaNacimiento_year"))+"-"+str(request.POST.get("fechaNacimiento_month"))+"-"+str(request.POST.get("fechaNacimiento_day"))
			
			userEgre.promoteAge=int(request.POST.get("graduacion"))
			userEgre.genero=request.POST.get("genero")
			
			if(request.POST.get("direccionResidencia") is not None):
				userAdminEgre.direccionResidencia=request.POST.get("direccionResidencia")	
			
			if(request.POST.get("direccionTrabajo") is not None):
				userEgre.direccionTrabajo=request.POST.get("direccionTrabajo")
			
			if(request.POST.get("ocupacionActual") is not None):
				userEgre.ocupacionActual=request.POST.get("ocupacionActual")
			
			if(request.POST.get("telefono") is not None):
				userAdminEgre.telefono=request.POST.get("telefono")
				
			userEgre.privacidad=request.POST.get("privacidad")
			user.set_password(request.POST.get("password"))
			
			user.save()
			userAdminEgre.save()
			userEgre.save()
			messages.success(request, 'Se ha actualizado su cuenta')
			user = authenticate(username=request.user, password=request.POST.get("password"))
			login(request, user)
			return redirect("usuarioEgre:index")
		else:
			messages.error(request, 'Hay errores en el registro, revise los campos')
	return render(request, 'egresado/primerlogin.html',context)