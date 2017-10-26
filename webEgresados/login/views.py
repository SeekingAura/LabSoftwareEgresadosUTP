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
from usuarioEgresado.models import UsuarioEgresado
from django.contrib.auth import authenticate, login

#Entry.objects.get(pk=1)#hacer querys antes de esto


def determinarTipoUser(username):
	user=User.objects.get(username=username)
	user=UsuariosAdminEgresado.objects.get(user_id=user.id)
	try:
		userAdmin=UsuarioAdministrador.objects.get(userAdminEgre_id=user.DNI)
	except:
		userAdmin=None
	
	try:
		userEgre=UsuarioEgresado.objects.get(userAdminEgre_id=user.DNI)
	except:
		userEgre=None
	
	if(userAdmin is not None and userEgre is not None):
		return ["egresado", "administrador"]
	elif(userAdmin is not None):
		return ["administrador"]
	elif(userEgre is not None):
		return["egresado"]
	elif(userAdmin is None and userEgre is None):
		print("ERROR - No se ha logrado determinar el tipo de usuario")
		return []
	
	#user=
	

def registro(request, type):
	context = {
		'type': type,
	}
	if(type=="admin"):
		form = registroAdministrador()
		context['form'] = form
	elif(type=="egresado"):
		form = registroEgresado()
		context['form'] = form
		
	
	if(request.method == 'POST'):
		
		if(type=="admin"):
			form=registroAdministrador(data=request.POST)
			context['form'] = form
		elif(type=="egresado"):
			form=registroEgresado(data=request.POST)
			context['form'] = form
		if(form.is_valid()):
			print("es valido, creando user")
			user=User.objects.create(username=str(request.POST.get("username")).lower(), email=str(request.POST.get("username")).lower(),first_name=str(request.POST.get("first_name")).title(), last_name=str(request.POST.get("last_name")).title())
			
			#user.set_password(request.POST.get("password"))
			user.set_password("123")
			user.save()
			
			#
			userAdminEgre=UsuariosAdminEgresado.objects.create(user=user, DNI=request.POST.get("DNI"), estadoCuenta="pendiente")
			
			userAdminEgre.save()
			
			#
			if(type=="admin"):
				userAdmin=UsuarioAdministrador.objects.create(userAdminEgre=userAdminEgre)
				userAdmin.save()
				form = registroAdministrador()
				context['form'] = form
			elif(type=="egresado"):
				userEgre=UsuarioEgresado.objects.create(userAdminEgre=userAdminEgre, programa=request.POST.get("programa"))
				userEgre.save()
				form = registroEgresado()
				context['form'] = form
			messages.success(request, 'registro completado con exito')
			
		
	
	return render(request,'usuarios/registro.html', context)

def login_view(request):
	context={}
	form=loginForm()
	context['form'] = form
	if(request.method == 'POST'):
		form=loginForm(data=request.POST)
		context['form'] = form
		if(form.is_valid()):
			user = form.login(request)
			if user:
				login(request, user)
				tipoUser=determinarTipoUser(user)
				if(len(tipoUser)==2):
					print("este usuario es Admin y Egresado")
				elif(tipoUser[0]=="administrador"):
					print("este usuario es Admin")
				elif(tipoUser[0]=="egresado"):
					print("este usuario es egresado")
				return HttpResponseRedirect("bienvenido")
	return render(request,'login.html', context)

	
	
@login_required(login_url="usuario:login")
def Bienvenido(request):
	
	username = None
	context={'username': username, 'tipoUser' : None, 'user' : request.user}
	if request.user.is_authenticated():
		username = request.user.first_name
		context['username']=username
		tipoUser=determinarTipoUser(request.user)
		if(len(tipoUser)==2):
			print("este usuario es Admin y Egresado")
			context['tipoUser']="Administrador y/o Egresado"
		elif(tipoUser[0]=="administrador"):
			print("este usuario es Admin")
			context['tipoUser']="Administrador"
		elif(tipoUser[0]=="egresado"):
			print("este usuario es egresado")
			context['tipoUser']="Egresado"
		print(UsuariosAdminEgresado.objects.all().filter(estadoCuenta="pendiente"))
		#for i in rang
		
	return render_to_response('bienvenido.html',context)

	
def logout_view(request):
	logout(request)
	print("Trate de LOGOUT")
	return redirect("usuario:login")# Redirect to a success page.
	#return HttpResponseRedirect("login")
	
	
def index(request):
	return render(request, 'index/oxygen/index.html', {})

#def index(request):
	#return HttpResponse("aqui estoy en index del login")