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
from .forms import primerLogin_Form
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
	print("estoy en primer inicio")
	return render(request, 'egresado/primerlogin.html',context)