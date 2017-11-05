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
from django.core.mail import EmailMessage


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

def redirectAdmin(user):
	tipoUser=determinarTipoUser(user)
	if(len(tipoUser)==2):
		#print("este usuario es Admin y Egresado")
		return None
	elif(tipoUser[0]=="administrador"):
		#print("este usuario es Admin")
		return None
	elif(tipoUser[0]=="egresado"):
		#print("este usuario es egresado")
		return redirect("usuarioEgre:index")
	return None
		
@login_required(login_url="usuario:login")		
def aceptarSoli_view(request, DNI):
	redirectValue=redirectAdmin(request.user)
	if(redirectValue is not None):#caso para redireccionar si entra usuario que no es admin
		return redirectValue
	print("Aceptando soli", DNI)
	try:
		userAdminEgre=UsuariosAdminEgresado.objects.get(DNI=str(DNI))
		if(userAdminEgre.estadoCuenta=="pendiente"):
			userAdminEgre.estadoCuenta="activada"
			userAdminEgre.save()
			user=User.objects.get(id=userAdminEgre.user_id)
			password=User.objects.make_random_password()
			user.set_password(password)
			user.save()
			email = EmailMessage("Activación de cuenta", "Su cuenta ha sido ACTIVADA satisfactoriamente, recuerde que debe ingresar a http://"+str(request.META['HTTP_HOST'])+"/usuario/login para acceder a su cuenta \n\nSu usuario es: "+str(user.email)+"\nsu contraseña es: "+str(password), to=[str(user.email)])
			#email.send()#Descomentar para que envie mensaje
			messages.success(request, 'Usuario con DNI: '+str(DNI)+" Aceptado correctamente")
	except:
		print("NOT FOUND")
	return redirect("usuarioAdmin:index")

	
def rechazarSoli_view(request, DNI):
	redirectValue=redirectAdmin(request.user)
	if(redirectValue is not None):#caso para redireccionar si entra usuario que no es admin
		return redirectValue
	print("Rechazando soli", DNI)
	try:
		userAdminEgre=UsuariosAdminEgresado.objects.get(DNI=str(DNI))
		if(userAdminEgre.estadoCuenta=="pendiente"):
			userAdminEgre.estadoCuenta="rechazada"
			userAdminEgre.save()
			user=User.objects.get(id=userAdminEgre.user_id)
			#password=User.objects.make_random_password()
			#user.set_password(password)
			#user.save()
			mensaje=""
			email = EmailMessage("Activación de cuenta", "Su cuenta ha sido RECHAZADA, por el motivo de: "+mensaje+" \n\nSi desea formar parte del sistema solvente los problemas planteados en su motivo de rechazo, Para mayor información consulte con un administrador", to=[str(user.email)])
			#email.send()#Descomentar para que envie mensaje
			User.objects.get(id=userAdminEgre.user_id).delete()
			messages.warning(request, 'Usuario con DNI: '+str(DNI)+" Rechazado correctamente")
	except:
		print("NOT FOUND")
	return redirect("usuarioAdmin:index")
		
@login_required(login_url="usuario:login")
def index(request):
	redirectValue=redirectAdmin(request.user)
	if(redirectValue is not None):#caso para redireccionar si entra usuario que no es admin
		return redirectValue
	username = None
	context={'username': username, 'tipoUser' : "Administrador", 'user' : request.user}
	if request.user.is_authenticated():
		username = request.user.first_name
		context['username']=username
		solicPendientes=UsuariosAdminEgresado.objects.all().filter(estadoCuenta="pendiente")
		#print(solicPendientes)
		listSoli=[]
		for i in solicPendientes:
			listSoli.append([i.DNI, i.user_id])
		listSoliEgre=[]
		for i in listSoli:
			try:
				tempEgre=UsuarioEgresado.objects.get(userAdminEgre_id=i[0])
				tempUser=User.objects.get(id=i[1])
				listSoliEgre.append([tempUser, tempEgre, i[0]])
			except:
				continue
		context['listSolicitudes']=listSoliEgre
	return render(request,'administrador/solicitudes.html', context)