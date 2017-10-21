from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader


from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .forms import registroAdministrador, registroEgresado
from django.contrib.auth.decorators import login_required
from django.core.validators import EmailValidator, ValidationError
from django.contrib import messages

from usuarioAdminEgresado.models import UsuariosAdminEgresado
from usuarioAdministrador.models import UsuarioAdministrador
from usuarioEgresado.models import UsuariosEgresado


#Entry.objects.get(pk=1)#hacer querys antes de esto

	

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
		
	if(request.method == 'GET'):
		print("haciendo get")
		#messages.error(request, "Error!")
		if(type=="admin"):
			#form.run_validators(request.GET)
			form=registroAdministrador(data=request.GET)
			print("toma de datos admin", form.is_valid(), request.GET, request.GET.get("username"))
			
		elif(type=="egresado"):
			form=registroEgresado(data=request.GET)
		else:
			raise ValidationError('type {} no reconocible al registrar'.format(type))
		if(form.is_valid()):
			user=User.objects.create(username=request.GET.get("username"), email=request.GET.get("username"))
			user.set_password(request.GET.get("password"))
			print("formulario es valido, valores {}, {}, {}",format(request.GET.get("username"), request.GET.get("password"), request.GET.get("first_name")))
	
	
	if(request.method == 'POST'):
		
		if(type=="admin"):
			#form.run_validators(request.GET)
			form=registroAdministrador(data=request.POST)
			context['form'] = form
			print("toma de datos admin", form.is_valid(), request.POST, request.POST.get("username"))
		
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
			
			
		
	else:
		return render(request,'usuarios/registro.html', context)
	
	return render(request,'usuarios/registro.html', context)
"""
class RegistroUsuario(CreateView):
	model = User
	template_name = "registrar.html"
	form_class = RegistroForm
	success_url = reverse_lazy("login")
"""

@login_required
def Bienvenido(request):	
	return render_to_response('bienvenido.html',{})

def index(request):
    return render(request, 'index/index.html', {})

#def index(request):
	#return HttpResponse("aqui estoy en index del login")