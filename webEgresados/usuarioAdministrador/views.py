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

from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from usuarioAdminEgresado.models import UsuariosAdminEgresado
from usuarioAdministrador.models import UsuarioAdministrador, noticias, noticiasIntereses, intereses
from usuarioAdministrador.forms import crearNoticia_Form, modificarNoticia_Form, getIntereses, primerLogin_Form, getDepartamentos, editarPerfil_Form
from usuarioEgresado.models import UsuarioEgresado
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from .decorators import *
import datetime
import re

#validators
def numeric_validator(value):
	result=re.match('[0-9]*', str(value))
	if result is not None:	
		
		if len(result.group(0))!=len(str(value)):
			
			#raise ValidationError('este campo debe ser solamente númerico')
			return True
	else:
		
		#raise ValidationError('este campo debe ser solamente númerico')
		return True
	return False
	
def noticiaAlreadyExist_validator(value):
	value=value.lower()
	
	temp=noticias.objects.all().values_list('titulo')
	for i in temp:
		if str(i[0]).lower()==value:
			#raise ValidationError('Ya existe una noticia con dicho nombre')
			return True
	return False
			
def getAllNoticias():
	tempValues=noticias.objects.all()
	result=[]
	for i in tempValues:
		temp=[i.titulo, i.contenido, [], i.creador.userAdminEgre.user.first_name+" "+i.creador.userAdminEgre.user.last_name, str(i.fechaCreacion)+" - "+str(i.timeCreacion.strftime('%H:%M:%S')), str(i.fechaEdicion)+" - "+str(i.timeEdicion.strftime('%H:%M:%S'))]
		tempInteresesNoticia=noticiasIntereses.objects.all().filter(noticia=i)
		for j in tempInteresesNoticia:
			temp[2].append(j.interes)
		result.append(temp)
	return result

def getOtherNoticias(userId):
	user=User.objects.get(id=userId)
	userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
	userAdmin=UsuarioAdministrador.objects.get(userAdminEgre_id=userAdminEgre.DNI)
	tempValues=noticias.objects.all().exclude(creador_id=userAdmin.id)
	result=[]
	for i in tempValues:
		temp=[i.titulo, i.contenido, [], i.creador.userAdminEgre.user.first_name+" "+i.creador.userAdminEgre.user.last_name, str(i.fechaCreacion)+" - "+str(i.timeCreacion.strftime('%H:%M:%S')), str(i.fechaEdicion)+" - "+str(i.timeEdicion.strftime('%H:%M:%S'))]
		
		tempInteresesNoticia=noticiasIntereses.objects.all().filter(noticia=i)
		for j in tempInteresesNoticia:
			temp[2].append(j.interes)
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
		temp=[i.titulo, i.contenido, [], i.id, str(i.fechaCreacion)+" - "+str(i.timeCreacion.strftime('%H:%M:%S')), str(i.fechaEdicion)+" - "+str(i.timeEdicion.strftime('%H:%M:%S'))]
		tempInteresesNoticia=noticiasIntereses.objects.all().filter(noticia=i)
		for j in tempInteresesNoticia:
			temp[2].append(j.interes)
		result.append(temp)
	return result


	
@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
@primerLogin(index_url="usuarioAdmin:primerLogin")
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
@primerLogin(index_url="usuarioAdmin:primerLogin")
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
			mensaje=""#debe ser algo que se capture al realziar rechazo
			email = EmailMessage("Activación de cuenta", "Su cuenta ha sido RECHAZADA, por el motivo de: "+mensaje+" \n\nSi desea formar parte del sistema solvente los problemas planteados en su motivo de rechazo, Para mayor información consulte con un administrador", to=[str(user.email)])
			#email.send()#MODO_PRUEBAS
			User.objects.get(id=userAdminEgre.user_id).delete()
			messages.warning(request, 'Usuario con DNI: '+str(DNI)+" Rechazado correctamente")
	except:
		print("NOT FOUND")
	return redirect("usuarioAdmin:index")
		
@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
@primerLogin(index_url="usuarioAdmin:primerLogin")
def solicitudes_view(request):
	username = None
	context={'username': username, 'tipoUser' : "Administrador", 'user' : request.user}
	if request.user.is_authenticated():
		username = request.user.first_name
		context['username']=username
		solicPendientes=UsuariosAdminEgresado.objects.all().filter(estadoCuenta="pendiente")
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
@primerLogin(index_url="usuarioAdmin:primerLogin")
def crearNoticias_view(request):
	username = None
	context={'username': request.user.first_name, 'tipoUser' : "Administrador", 'user' : request.user}
	form = crearNoticia_Form()
	form_intereses = getIntereses()
	context['form'] = form
	context['intereses'] = form_intereses
		
	
	if(request.method == 'POST'):
		form=crearNoticia_Form(data=request.POST)
		context['form'] = form
		context['intereses'] = form_intereses
		valido=True
		if(len(request.POST.getlist("intereses"))==0):
			messages.error(request, 'Debe tener seleccionado al menos 1 interes')
			valido=False
		if(noticiaAlreadyExist_validator(request.POST.get("titulo"))):
			messages.error(request, 'El titulo que se indicó para la noticia ya existe en el sistema')
			valido=False
		if(form.is_valid() and valido):
			print("es valido, creando noticia")
			
			userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=request.user.id)
			userAdmin=UsuarioAdministrador.objects.get(userAdminEgre_id=userAdminEgre.DNI)
			noticia=noticias.objects.create(titulo=request.POST.get("titulo"), contenido=request.POST.get("contenido"), creador=userAdmin, fechaCreacion=datetime.datetime.now(), timeCreacion=datetime.datetime.now(), fechaEdicion=datetime.datetime.now(), timeEdicion=datetime.datetime.now())
			noticia.save()
			print("INTERESES: ", request.POST.getlist("intereses"))
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
@primerLogin(index_url="usuarioAdmin:primerLogin")
def editarNoticia_view(request, idNoticia):
	try:
		context={}
		noticia=noticias.objects.get(id=idNoticia)
		noticiasInteres=noticiasIntereses.objects.all().filter(noticia=noticia).values_list('interes')
		misIntereses=[]
		for i in noticiasInteres:
			misIntereses.append(i[0])
		form = modificarNoticia_Form(initial={'titulo':noticia.titulo, 'contenido':noticia.contenido, 'intereses': misIntereses})
		form_intereses = getIntereses()
		context['form'] = form
		context['noticia'] = noticia 
		context['misIntereses'] = misIntereses
		context['intereses'] = form_intereses

		noticiasTodas=noticias.objects.all().values_list('titulo')
		
		
		if(request.method == 'POST'):
			form=modificarNoticia_Form(data=request.POST)
			context['form'] = form
			context['noticia'] = request.POST 
			context['misIntereses'] = request.POST.getlist("intereses")
			context['intereses'] = form_intereses
			yaExiste=False
			for i in noticiasTodas:
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
				noticia.fechaEdicion=datetime.datetime.now()
				noticia.timeEdicion=datetime.datetime.now()
				noticia.save()	
				messages.success(request, 'Noticia editada!')
				form = crearNoticia_Form()
				context['form'] = form
				return redirect("usuarioAdmin:mostrarMisNoticias")
		return render(request,'administrador/modificarNoticia.html', context)
	except:
		messages.error(request, 'Error al modificar noticia, no existe')
		return redirect("usuarioAdmin:mostrarMisNoticias")
	
	
@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
@primerLogin(index_url="usuarioAdmin:primerLogin")
def eliminarNoticia_view(request, idNoticia):
	try:
		noticias.objects.get(id=idNoticia).delete()
		messages.error(request, 'Noticia borrada!')
	except:
		print("NOT FOUND")
	return redirect("usuarioAdmin:mostrarMisNoticias")
	
@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
@primerLogin(index_url="usuarioAdmin:primerLogin")
def verNoticiasPropias_view(request):
	username = None
	context={'username': request.user.first_name, 'tipoUser' : "Administrador", 'user' : request.user}
	context['noticias']=getAdminNoticias(request.user.id)
	
	
	return render(request,'administrador/mostrarMisNoticias.html', context)
	
@login_required(login_url="usuario:login")
@redirectAdmin(index_url="usuarioEgre:index")
@primerLogin(index_url="usuarioAdmin:primerLogin")
def verNoticiasTodas_view(request):
	username = None
	context={'username': request.user.first_name, 'tipoUser' : "Administrador", 'user' : request.user}
	context['noticias']=getOtherNoticias(request.user.id)
	
	
	return render(request,'administrador/mostrarTodasNoticias.html', context)

@login_required(login_url="usuario:login")
@primerLogin(index_url="usuarioAdmin:index", isNotYet=False)
@redirectAdmin(index_url="usuarioEgre:index")
def primerLogin_view(request):
	context={}
	form=primerLogin_Form()
	departamentos = getDepartamentos()
	form_intereses = getIntereses()
	context['form'] = form
	context['deptos'] = departamentos
	context['intereses'] = form_intereses
	context['datos'] = {}

	if(request.method == 'POST'):
		form=primerLogin_Form(data=request.POST)
		context['form'] = form
		context['datos'] = request.POST

		valido=True

		if(numeric_validator(request.POST.get("telefono"))):
			messages.error(request, 'El campo del telefono debe de ser númerico')
			valido=False
		if(request.POST.get("departamento")=="None"):
			messages.error(request, 'Debe elegir algun departamento')
			valido=False
			
		password1 = request.POST.get('password')
		password2 = request.POST.get('passwordConfimation')
		#print("cleaned password1={}, password2={}".format(password1, password2))
		if password1 != password2 and password2 is not None:
			messages.error(request, 'las contraseñas no coinciden') 
			valido=False
		else:
			try:
				validate_password(password1)
			except:
				messages.error(request, "su contraseña NO puede ser solamente númerica ni muy simple")
			
		if(form.is_valid() and valido):
			user=User.objects.get(username=request.user)
			userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
			
			userAdminEgre.pais="Colombia"
			userAdminEgre.departamento=request.POST.get("departamento")
			
			
			if(request.POST.get("direccionResidencia") is not None):
				userAdminEgre.direccionResidencia=request.POST.get("direccionResidencia")	
			
			
			if(request.POST.get("telefono") is not None):
				userAdminEgre.telefono=request.POST.get("telefono")
				
			user.set_password(request.POST.get("password"))
			
			user.save()
			userAdminEgre.save()
			messages.success(request, 'Se ha actualizado su cuenta')
			user = authenticate(username=request.user, password=request.POST.get("password"))
			login(request, user)
			return redirect("usuarioAdmin:index")
		else:
			messages.error(request, 'Hay errores en el registro, revise los campos')
	return render(request, 'administrador/primerlogin.html',context)

@login_required(login_url="usuario:login")
@primerLogin(index_url="usuarioEgre:primerLogin")
@redirectAdmin(index_url="usuarioEgre:index")
def editarPerfil_view(request):
	context={}

	user=User.objects.get(id=request.user.id)
	userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
	form = editarPerfil_Form(initial={'direccionResidencia':userAdminEgre.direccionResidencia, 'telefono': userAdminEgre.telefono})
	context['form'] = form
	context['userAdminEgre'] = userAdminEgre
	
	if(request.method == 'POST'):
		form=editarPerfil_Form(data=request.POST)
		context['form'] = form
		valido=True
		
		
		if(numeric_validator(request.POST.get("telefono"))):
			messages.error(request, 'El campo del telefono debe de ser númerico')
			valido=False
		
		password1 = request.POST.get('password')
		password2 = request.POST.get('passwordConfimation')
		#print("cleaned password1={}, password2={}".format(password1, password2))
		if password1 != password2 and password2 is not None:
			messages.error(request, 'las contraseñas no coinciden') 
			valido=False
		else:
			try:
				validate_password(password1)
			except:
				messages.error(request, "su contraseña NO puede ser solamente númerica ni muy simple")
		
		if(form.is_valid() and valido):
			user=User.objects.get(username=request.user)
			userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
			
			userAdminEgre.direccionResidencia=request.POST.get("direccionResidencia")	
			
			userAdminEgre.telefono=request.POST.get("telefono")
			
			user.set_password(request.POST.get("password"))
			usuarioActual=request.user
			logout(request)
			user.save()
			userAdminEgre.save()
			messages.success(request, 'Se ha actualizado su cuenta')
			user = authenticate(username=usuarioActual, password=request.POST.get("password"))
			login(request, user)
		else:
			messages.error(request, 'Hay errores en el registro, revise los campos')
	return render(request, 'administrador/editarPerfil.html',context)