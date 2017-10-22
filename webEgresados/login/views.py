from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader


from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .forms import registroAdministrador, registroEgresado, loginForm
from django.contrib.auth.decorators import login_required
from django.core.validators import EmailValidator, ValidationError
from django.contrib import messages

from usuarioAdminEgresado.models import UsuariosAdminEgresado
from usuarioAdministrador.models import UsuarioAdministrador
from usuarioEgresado.models import UsuariosEgresado
from django.contrib.auth import authenticate, login

#Entry.objects.get(pk=1)#hacer querys antes de esto


def determinarTipoUser(username):
	print("")
	

def registro(request, type):
	context = {
		'type': type,
	}
	if(type=="admin"):
		form = registroAdministrador()
		context['form'] = form
	else:
		form = registroEgresado()
		context['form'] = form
		
	
	if(request.method == 'POST'):
		
		if(type=="admin"):
			form=registroAdministrador(data=request.POST)
			context['form'] = form
			#print("toma de datos admin", form.is_valid(), request.POST, request.POST.get("username"))
		
		if(form.is_valid()):
			print("es valido, creando user")
			user=User.objects.create(username=request.POST.get("username"), email=request.POST.get("username"),first_name=request.POST.get("first_name"), last_name=request.POST.get("last_name"))
			
			user.set_password(request.POST.get("password"))
			
			user.save()
			
			#
			userAdminEgre=UsuariosAdminEgresado.objects.create(user=user, DNI=request.POST.get("DNI"), estadoCuenta="Pendiente")
			
			userAdminEgre.save()
			
			#
			userAdmin=UsuarioAdministrador.objects.create(userEgre=userAdminEgre)
			userAdmin.save()
			if(type=="admin"):
				form = registroAdministrador()
				context['form'] = form
			else:
				form = registroEgresado()
				context['form'] = form
			messages.success(request, 'registro completado con exito')
			
		
	
	return render(request,'usuarios/registro.html', context)

def login_view(request):
	context={}
	form=loginForm()
	context['form'] = form
	#print("formulario entrante", form)
	#print("request login")
	if(request.method == 'POST'):
		form=loginForm(data=request.POST)
		context['form'] = form
		if(form.is_valid()):
			user = form.login(request)
			#print("usuario entra", user)
			if user:
				login(request, user)
				return HttpResponseRedirect("bienvenido")
	return render(request,'login.html', context)

	
	
@login_required(login_url="usuario:login")
def Bienvenido(request):
	
	username = None
	context={'username': username,}
	if request.user.is_authenticated():
		print("usuario logeado", request.user)
		#User.objects.get(username=request.user.username)
		username = request.user.first_name
		context['username']=username
		
		print("usuario logeado", username)
	return render_to_response('bienvenido.html',context)

	
def logout_view(request):
	logout(request)
	print("Trate de LOGOUT")
	return redirect("usuario:login")# Redirect to a success page.
	#return HttpResponseRedirect("login")
	
	
def index(request):
	return render(request, 'index/index.html', {})

#def index(request):
	#return HttpResponse("aqui estoy en index del login")