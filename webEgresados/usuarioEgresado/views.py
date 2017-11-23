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

from usuarioAdminEgresado.models import UsuariosAdminEgresado, Pais
from usuarioAdministrador.models import UsuarioAdministrador, intereses, noticias, noticiasIntereses
from usuarioEgresado.models import UsuarioEgresado, InteresesEgresado
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import password_validators_help_text_html
from .forms import primerLogin_Form, departamentoValidator, getPaises, getDepartamentos, getIntereses, editarPerfil_Form
from .decorators import *

from operator import attrgetter


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

def getInteresesEgresado(idUser):
	user=User.objects.get(id=idUser)
	userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
	userEgre=UsuarioEgresado.objects.get(userAdminEgre_id=userAdminEgre.DNI)
	return InteresesEgresado.objects.all().filter(userEgre_id=userEgre.id).values_list('interes')
	
def getImage(idUser):
	user=User.objects.get(id=idUser)
	userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
	userEgre=UsuarioEgresado.objects.get(userAdminEgre_id=userAdminEgre.DNI)
	return userEgre.foto
	
def getAllNoticiasSortedInteres(idUser):
	
	interesesRelacionados=getInteresesEgresado(idUser)
	tempValues=[]
	noticiasResultID=[]
	result=[]
	print(interesesRelacionados)
	for i in interesesRelacionados:#agregando id de noticias a razón de intereses
		temp=noticiasIntereses.objects.all().filter(interes=i).values_list('noticia')
		for j in temp:
			if not j[0] in noticiasResultID:
				noticiasResultID.append(j[0])
	
	for i in noticiasResultID:#agregando las noticias con los id obtenidos
		x=noticias.objects.get(id=i)
		tempValues.append(x)
	

	
	# noticias relacioandas al interes
	for i in sorted(tempValues, key=attrgetter('timeEdicion', 'fechaEdicion'), reverse=True):
		temp=[i.titulo, i.contenido, [], i.creador.userAdminEgre.user.first_name+" "+i.creador.userAdminEgre.user.last_name, str(i.fechaCreacion)+" - "+str(i.timeCreacion.strftime('%H:%M:%S')), str(i.fechaEdicion)+" - "+str(i.timeEdicion.strftime('%H:%M:%S'))]
		tempInteresesNoticia=noticiasIntereses.objects.all().filter(noticia=i)
		for j in tempInteresesNoticia:
			temp[2].append(j.interes)
		result.append(temp)
	
	noticiasResultIDtemp2=[]
	
	for i in noticiasIntereses.objects.all().values_list('noticia'):
		if not i[0] in noticiasResultID:#agregando id de las demas noticias
			noticiasResultID.append(i[0])
			noticiasResultIDtemp2.append(i[0])#lista de los valores restantes
	
	tempValues=[]
	for i in noticiasResultIDtemp2:#agregando las noticias con los id obtenidos
		x=noticias.objects.get(id=i)
		tempValues.append(x)
	
	for i in sorted(tempValues, key=attrgetter('timeEdicion','fechaEdicion'), reverse=True):
		temp=[i.titulo, i.contenido, [], i.creador.userAdminEgre.user.first_name+" "+i.creador.userAdminEgre.user.last_name, str(i.fechaCreacion)+" - "+str(i.timeCreacion.strftime('%H:%M:%S')), str(i.fechaEdicion)+" - "+str(i.timeEdicion.strftime('%H:%M:%S'))]
		tempInteresesNoticia=noticiasIntereses.objects.all().filter(noticia=i)
		for j in tempInteresesNoticia:
			temp[2].append(j.interes)
		result.append(temp)
	
	return result


	
@login_required(login_url="usuario:login")
@primerLogin(index_url="usuarioEgre:primerLogin")
@redirectEgresado(index_url="usuarioAdmin:index")
def index_view(request):
	username = None
	context={'username': username, 'tipoUser' : "Egresado", 'user' : request.user}
	username = request.user.first_name
	context['username']=username
	
	return render(request, 'egresado/index.html',context)

@login_required(login_url="usuario:login")
@primerLogin(index_url="usuarioEgre:index", isNotYet=False)
@redirectEgresado(index_url="usuarioAdmin:index")
def primerLogin_view(request):
	context={}
	form=primerLogin_Form()
	paises = getPaises()
	departamentos = getDepartamentos()
	intereses = getIntereses()
	context['form'] = form
	context['paises'] = paises
	context['deptos'] = departamentos
	context['intereses'] = intereses
	if(request.method == 'POST'):
		print(request.POST)
		p = request.POST.get('pais')
		print("PAISSSSSSSSSSS " + p) 	
		form=primerLogin_Form(data=request.POST)
		context['form'] = form
		context['paises'] = paises
		context['deptos'] = departamentos
		context['intereses'] = intereses

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
	
@login_required(login_url="usuario:login")
@primerLogin(index_url="usuarioEgre:primerLogin")
@redirectEgresado(index_url="usuarioAdmin:index")
def verNoticias_view(request):
	username = None
	context={'username': username, 'tipoUser' : "Egresado", 'user' : request.user}
	username = request.user.first_name
	context['username']="probando"
	interesesValue=getInteresesEgresado(request.user.id)
	context['noticias']=getAllNoticiasSortedInteres(request.user.id)
		
	return render(request, 'egresado/NoticiasTodas.html',context)

@login_required(login_url="usuario:login")
@primerLogin(index_url="usuarioEgre:primerLogin")
@redirectEgresado(index_url="usuarioAdmin:index")
def editarPerfil_view(request):
	context={}

	user=User.objects.get(id=request.user.id)
	userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
	userEgre=UsuarioEgresado.objects.get(userAdminEgre_id=userAdminEgre.DNI)
	interesesDato=InteresesEgresado.objects.all().filter(userEgre=userEgre).values_list("interes")
	print(interesesDato)
	interesesDatoTemp=[]
	for i in interesesDato:
		interesesDatoTemp.append(i[0])
	print(interesesDatoTemp)
	form = editarPerfil_Form(initial={'intereses':interesesDatoTemp, 'direccionResidencia':userAdminEgre.direccionResidencia, 'direccionTrabajo': userEgre.direccionTrabajo, 'ocupacionActual': userEgre.ocupacionActual, 'telefono': userAdminEgre.telefono, 'privacidad': userEgre.privacidad, 'foto':userEgre.foto})
	context['form'] = form
	print(userEgre.foto)
	
	if(request.method == 'POST'):
		form=editarPerfil_Form(data=request.POST, files=request.FILES)
		
		context['form'] = form
		valido=True
		
		if(len(request.POST.getlist("intereses"))==0):
			messages.error(request, 'Debe tener seleccionado al menos 1 interes')
			valido=False
		if(form.is_valid() and valido):
			user=User.objects.get(username=request.user)
			userAdminEgre=UsuariosAdminEgresado.objects.get(user_id=user.id)
			userEgre=UsuarioEgresado.objects.get(userAdminEgre_id=userAdminEgre.DNI)
			
			InteresesEgresado.objects.all().filter(userEgre=userEgre).delete()
			for i in request.POST.getlist("intereses"):
				interes=intereses.objects.get(titulo=i)
				interes=InteresesEgresado.objects.create(userEgre=userEgre, interes=interes)
				interes.save()

			
			userAdminEgre.direccionResidencia=request.POST.get("direccionResidencia")	
			
			userEgre.direccionTrabajo=request.POST.get("direccionTrabajo")
			
			userEgre.ocupacionActual=request.POST.get("ocupacionActual")
			
			userAdminEgre.telefono=request.POST.get("telefono")
			
			userEgre.foto=request.POST.get("foto")
			print(request.FILES)
			print(form.cleaned_data)
			userEgre.privacidad=request.POST.get("privacidad")
			user.set_password(request.POST.get("password"))
			usuarioActual=request.user
			logout(request)
			user.save()
			userAdminEgre.save()
			userEgre.save()
			messages.success(request, 'Se ha actualizado su cuenta')
			user = authenticate(username=usuarioActual, password=request.POST.get("password"))
			login(request, user)
		else:
			messages.error(request, 'Hay errores en el registro, revise los campos')
	return render(request, 'egresado/editarPerfil.html',context)
