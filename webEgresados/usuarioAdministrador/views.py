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
from usuarioAdministrador.models import UsuarioAdministrador, noticias, noticiasIntereses, intereses
from usuarioAdministrador.forms import crearNoticia_Form, modificarNoticia_Form
from usuarioEgresado.models import UsuarioEgresado
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from .decorators import *


def getAllNoticias():
	tempValues=noticias.objects.all()
	result=[]
	for i in tempValues:
		temp=[i.titulo, i.contenido]
		result.append(temp)
	print(result)
	return result

def getOtherNoticias(userId):
	user=User.objects.get(id=userId)
	userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
	userAdmin=UsuarioAdministrador.objects.get(userAdminEgre_id=userAdminEgre.DNI)
	tempValues=noticias.objects.all().exclude(creador_id=userAdmin.id)
	result=[]
	for i in tempValues:
		temp=[i.titulo, i.contenido]
		result.append(temp)
	print(result)
	return result

def getAdminNoticias(userId):
	user=User.objects.get(id=userId)
	userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
	userAdmin=UsuarioAdministrador.objects.get(userAdminEgre_id=userAdminEgre.DNI)
	tempValues=noticias.objects.all().filter(creador_id=userAdmin.id)
	
	result=[]
	for i in tempValues:
		temp=[i.titulo, i.contenido, [], i.id]
		tempInteresesNoticia=noticiasIntereses.objects.all().filter(noticia=i)
		for j in tempInteresesNoticia:
			temp[2].append(j.interes)
		result.append(temp)
	return result


	
@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
def aceptarSoli_view(request, DNI):
	print("Aceptando soli", DNI)
	try:
		userAdminEgre=UsuariosAdminEgresado.objects.get(DNI=str(DNI))
		if(userAdminEgre.estadoCuenta=="pendiente"):
			userAdminEgre.estadoCuenta="activada"
			userAdminEgre.save()
			user=User.objects.get(id=userAdminEgre.user_id)
			password=User.objects.make_random_password()
			#user.set_password(password)
			user.set_password("123")
			user.save()
			email = EmailMessage("Activación de cuenta", "Su cuenta ha sido ACTIVADA satisfactoriamente, recuerde que debe ingresar a http://"+str(request.META['HTTP_HOST'])+"/usuario/login para acceder a su cuenta \n\nSu usuario es: "+str(user.email)+"\nsu contraseña es: "+str(password), to=[str(user.email)])
			#email.send()#MODO_PRUEBAS
			messages.success(request, 'Usuario con DNI: '+str(DNI)+" Aceptado correctamente")
	except:
		print("NOT FOUND")
	return redirect("usuarioAdmin:index")

@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
def rechazarSoli_view(request, DNI):
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
			#email.send()#MODO_PRUEBAS
			User.objects.get(id=userAdminEgre.user_id).delete()
			messages.warning(request, 'Usuario con DNI: '+str(DNI)+" Rechazado correctamente")
	except:
		print("NOT FOUND")
	return redirect("usuarioAdmin:index")
		
@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
def solicitudes_view(request):
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
	
@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
def crearNoticias_view(request):
	username = None
	context={'username': request.user.first_name, 'tipoUser' : "Administrador", 'user' : request.user}
	form = crearNoticia_Form()
	context['form'] = form
		
	
	if(request.method == 'POST'):
		form=crearNoticia_Form(data=request.POST)
		context['form'] = form
		if(len(request.POST.getlist("intereses"))==0):
			messages.error(request, 'Debe tener seleccionado al menos 1 interes')
		elif(form.is_valid()):
			print("es valido, creando noticia")
			
			userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=request.user.id)
			userAdmin=UsuarioAdministrador.objects.get(userAdminEgre_id=userAdminEgre.DNI)
			noticia=noticias.objects.create(titulo=request.POST.get("titulo"), contenido=request.POST.get("contenido"), creador=userAdmin)
			noticia.save()
			
			for i in request.POST.getlist("intereses"):
				tempIntereses=intereses.objects.get(titulo=i)
				tempNoticiaInteres=noticiasIntereses.objects.create(noticia=noticia, interes=tempIntereses)
				tempNoticiaInteres.save()
			
				
			messages.success(request, 'Noticia creada!')
			form = crearNoticia_Form()
			context['form'] = form
		else:
			messages.error(request, 'Hay errores en los campos')
	return render(request,'administrador/crearNoticia.html', context)

@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
def editarNoticia_view(request, idNoticia):
	try:
		context={}
		noticia=noticias.objects.get(id=idNoticia)
		noticiasInteres=noticiasIntereses.objects.all().filter(noticia=noticia).values_list('interes')
		temp=[]
		for i in noticiasInteres:
			temp.append(i[0])
		form = modificarNoticia_Form(initial={'titulo':noticia.titulo, 'contenido':noticia.contenido, 'intereses': temp})
		context['form'] = form
		

		temp=noticias.objects.all().values_list('titulo')
		
		
		if(request.method == 'POST'):
			form=modificarNoticia_Form(data=request.POST)
			context['form'] = form
			yaExiste=False
			for i in temp:
				print(i)
				if str(i[0]).lower()==request.POST.get("titulo").lower():
					yaExiste=True
			print(str(noticia.titulo).lower(), str(request.POST.get("titulo").lower()))
			if(str(noticia.titulo).lower()!=str(request.POST.get("titulo")).lower() and yaExiste):
				
				messages.error(request, 'El nombre de la noticia ya existe')
			elif(len(request.POST.getlist("intereses"))==0):
				messages.error(request, 'Debe tener seleccionado al menos 1 interes')
			elif(form.is_valid()):
				noticia.titulo=request.POST.get("titulo")
				noticia.contenido=request.POST.get("contenido")
				noticiasIntereses.objects.all().filter(noticia=noticia).delete()
				
				for i in request.POST.getlist("intereses"):
					tempIntereses=intereses.objects.get(titulo=i)
					tempNoticiaInteres=noticiasIntereses.objects.create(noticia=noticia, interes=tempIntereses)
					tempNoticiaInteres.save()
				noticia.save()	
				messages.success(request, 'Noticia editada!')
				form = crearNoticia_Form()
				context['form'] = form
				return redirect("usuarioAdmin:mostrarMisNoticias")
		return render(request,'administrador/crearNoticia.html', context)
	except:
		messages.error(request, 'Error al modificar noticia, no existe')
		return redirect("usuarioAdmin:mostrarMisNoticias")
	
	
@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
def eliminarNoticia_view(request, idNoticia):
	try:
		noticias.objects.get(id=idNoticia).delete()
		messages.warning(request, 'Noticia borrada!')
	except:
		print("NOT FOUND")
	return redirect("usuarioAdmin:mostrarMisNoticias")
	
@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
def verNoticiasPropias_view(request):
	username = None
	context={'username': request.user.first_name, 'tipoUser' : "Administrador", 'user' : request.user}
	context['noticias']=getAdminNoticias(request.user.id)
	
	
	return render(request,'administrador/mostrarMisNoticias.html', context)