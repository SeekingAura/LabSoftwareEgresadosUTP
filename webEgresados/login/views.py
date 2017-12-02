from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader


from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .forms import registroAdministrador, registroEgresado, loginForm, loginSudo_Form, crearInteres_Form
from django.contrib.auth.decorators import login_required
from django.core.validators import EmailValidator, ValidationError
from django.contrib import messages

from usuarioAdminEgresado.models import UsuariosAdminEgresado
from usuarioAdministrador.models import UsuarioAdministrador, intereses
from usuarioEgresado.models import UsuarioEgresado
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
#Entry.objects.get(pk=1)#hacer querys antes de esto


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
			#user.set_password("123")
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
				email = EmailMessage("Registro de cuenta", "Su cuenta ha quedado pendiente a ser activada por un Super usuario, esté atento a que su solicitud sea atendida \n\nNo olvide que su cuenta es "+str(request.POST.get("username")).lower(), to=[str(request.POST.get("username")).lower()])
				#email.send()#MODO_PRUEBAS
				#user.set_password("123")#MODO_PRUEBAS
				user.save()#MODO_PRUEBAS
			elif(type=="egresado"):
				userEgre=UsuarioEgresado.objects.create(userAdminEgre=userAdminEgre, programa=request.POST.get("programa"))
				userEgre.save()
				form = registroEgresado()
				context['form'] = form
				email = EmailMessage("Registro de cuenta", "Su cuenta ha quedado pendiente a ser activada por un administrador, esté atento a que su solicitud sea atendida \n\nNo olvide que su cuenta es: "+str(request.POST.get("username")).lower(), to=[str(request.POST.get("username")).lower()])
				#email.send()#MODO_PRUEBAS
				
			messages.success(request, 'Registro completado con exito, se le ha enviado un mensaje a su correo electronico')
		#else:
			#messages.error(request, 'Hay errores en el registro')
		
	
	return render(request,'usuarios/registro.html', context)

def login_view(request):
	context={}
	form=loginForm()
	context['form'] = form
	if request.user.is_authenticated():#case if already logged
		username = request.user.first_name
		context['username']=username
		tipoUser=determinarTipoUser(request.user)
		
		if(not isinstance(tipoUser, list)):
			return redirect("usuario:sudoIndex")
		else:
			if(len(tipoUser)==2):
				return redirect("usuarioAdmin:index")
			elif(tipoUser[0]=="administrador"):
				return redirect("usuarioAdmin:index")
			elif(tipoUser[0]=="egresado"):
				return redirect("usuarioEgre:index")
	if(request.method == 'POST'):
		form=loginForm(data=request.POST)
		context['form'] = form
		if(form.is_valid()):
			user = form.login(request)
			if user:
				login(request, user)
				tipoUser=determinarTipoUser(user)
				if(len(tipoUser)==2):
					return redirect("usuarioAdmin:index")
				elif(tipoUser[0]=="administrador"):
					return redirect("usuarioAdmin:index")
				elif(tipoUser[0]=="egresado"):
					return redirect("usuarioEgre:index")
				
				return HttpResponseRedirect("bienvenido")
		
	return render(request,'login/login.html', context)

def loginSudo_view(request):
	context={}
	form=loginSudo_Form()
	context['form'] = form
	if request.user.is_authenticated():#case if already logged
		username = request.user.first_name
		context['username']=username
			
	if(request.method == 'POST'):
		form=loginSudo_Form(data=request.POST)
		context['form'] = form
		if(form.is_valid()):
			user = form.login(request)
			if user:
				login(request, user)
				return redirect("usuario:sudoIndex")
				
		
	return render(request,'sudo/login.html', context)

	
def indexSudo_view(request):
	context={}
	
	return render(request, 'sudo/index.html',context)

@login_required(login_url="usuario:sudoLogin")
def interesesTodosSudo_view(request):
	context={}
	datos=intereses.objects.all()
	for i in datos:
		i.titulo=i.titulo.replace(" ", "_")
	context['intereses']=datos
	return render(request, 'sudo/interesesTodos.html',context)

@login_required(login_url="usuario:sudoLogin")
def	interesEliminarSudo_view(request, idInteres):
	try:
		idInteres=idInteres.replace("_", " ")
		intereses.objects.get(titulo=idInteres).delete()
		messages.error(request, "Interes eliminado")
	except:
		print("Interes not found")
	return redirect("usuario:sudoInteresesVer")

@login_required(login_url="usuario:sudoLogin")
def interesCrearSudo_view(request):
	context={}
	form = crearInteres_Form()
	context['form'] = form

	if(request.method  == 'POST'):
		form = crearInteres_Form(data=request.POST)
		context['form'] = form
		valid = True
		print(request.POST)
		value = request.POST.get('titulo').lower()
		temp = intereses.objects.all().values_list('titulo')
		for i in temp:
			if str(i[0]).lower() == value:
				valid = False
				messages.error(request, 'Ya existe un interes con ese nombre')

		if(form.is_valid() and valid):
			interes = intereses.objects.create(titulo=request.POST.get('titulo'), description=request.POST.get('description'))
			interes.save()
			messages.success(request, 'Interes creado!!!')
			form = crearInteres_Form()
			context['form'] = form
			print("Pase por aqui")
		else:
			messages.error(request, 'Hay errores en los campos')
	return render(request, 'sudo/interesCrear.html',context)

@login_required(login_url="usuario:sudoLogin")
def interesEditarSudo_view(request, idInteres):
	context={}
	form = crearInteres_Form()
	try:
		idInteres=idInteres.replace("_", " ")
		interes=intereses.objects.get(titulo=idInteres)
	except:
		print("Interes not found")
	context['form'] = form
	context['interes']=interes
	

	if(request.method  == 'POST'):
		form = crearInteres_Form(data=request.POST)
		context['form'] = form
		valido = True
		value = request.POST.get('titulo').lower()
		interes.titulo=request.POST.get('titulo')
		interes.description=description=request.POST.get('description')
		context['interes']=interes
		if(str(interes.titulo.lower())!=value):
			temp = intereses.objects.all().values_list('titulo')
			for i in temp:
				if str(i[0]).lower() == value:
					valid = False
					messages.error(request, 'Ya existe un interes con ese nombre')
		
		if(form.is_valid() and valido):
			interes.titulo=request.POST.get('titulo')
			interes.description=description=request.POST.get('description')
			interes.save()
			messages.success(request, 'Interes modificado!!!')
			return redirect("usuario:sudoInteresesVer")
		else:
			messages.error(request, 'Hay errores en los campos')
	return render(request, 'sudo/interesEditar.html',context)
	
@login_required(login_url="usuario:sudoLogin")
def aceptarSoliSudo_view(request, DNI):
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
	return redirect("usuario:sudoSolicitudes")

@login_required(login_url="usuario:sudoLogin")
def rechazarSoliSudo_view(request, DNI):
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
			email = EmailMessage("Activación de cuenta", "Su cuenta ha sido RECHAZADA, por el motivo de: "+mensaje+" \n\nSi desea formar parte del sistema solvente los problemas planteados en su motivo de rechazo, Para mayor información consulte con el super usuario del sistema", to=[str(user.email)])
			#email.send()#MODO_PRUEBAS
			User.objects.get(id=userAdminEgre.user_id).delete()
			messages.warning(request, 'Usuario con DNI: '+str(DNI)+" Rechazado correctamente")
	except:
		print("NOT FOUND")
	return redirect("usuario:sudoSolicitudes")

	
@login_required(login_url="usuario:sudoLogin")
def solicitudesSudo_view(request):
	username = None
	context={'username': username, 'tipoUser' : "Administrador", 'user' : request.user}
	solicPendientes=UsuariosAdminEgresado.objects.all().filter(estadoCuenta="pendiente")
	listSoli=[]
	for i in solicPendientes:
		listSoli.append([i.DNI, i.user_id])
	listSoliAdmin=[]
	for i in listSoli:
		try:
			tempAdmin=UsuarioAdministrador.objects.get(userAdminEgre_id=i[0])
			tempUser=User.objects.get(id=i[1])
			listSoliAdmin.append([tempUser, tempAdmin, i[0]])
		except:
			continue
	context['listSolicitudes']=listSoliAdmin
	return render(request,'sudo/solicitudes.html', context)
	
	
def index_view(request):
	#username = None
	#context={'username': username, 'tipoUser' : "Egresado", 'user' : request.user}
	#username = request.user.first_name
	#context['username']=username
	
	return render(request, 'egresado/index.html',context)
	
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
		
		
	return render_to_response('login/bienvenido.html',context)

	
def logout_view(request):
	logout(request)
	return redirect("usuario:login")# Redirect to a success page.
	#return HttpResponseRedirect("login")
	
	
def index(request):
	return render(request, 'index/oxygen/index.html', {})

#def index(request):
	#return HttpResponse("aqui estoy en index del login")