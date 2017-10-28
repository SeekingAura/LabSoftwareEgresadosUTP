from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader


from django.contrib.auth import logout
from django.http import HttpResponseRedirect
#from .forms import registroAdministrador, registroEgresado, loginForm
from django.contrib.auth.decorators import login_required
from django.core.validators import EmailValidator, ValidationError
from django.contrib import messages

from usuarioAdminEgresado.models import UsuariosAdminEgresado
from usuarioAdministrador.models import UsuarioAdministrador
from usuarioEgresado.models import UsuarioEgresado
from django.contrib.auth import authenticate, login


def determinarTipoUser(username):
	try:
		user=User.objects.get(username=username)
		user=UsuariosAdminEgresado.objects.get(user_id=user.id)
	except:
		return redirect("usuario:login")
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

@login_required(login_url="usuario:login")
def index(request):
	
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
		
	return render_to_response('admin/index.html',context)