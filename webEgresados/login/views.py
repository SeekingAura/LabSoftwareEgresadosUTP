from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader


from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required
from django.core.validators import EmailValidator, ValidationError

def is_email(value):
	try:
		EmailValidator()(value)
	except ValidationError:
		return False
	else:
		return True

	
	
def registro(request):
	template=loader.get_template("registrar.html")
	if request.method == 'POST':
		form=RegistroForm(data=request.POST)
		if form.is_valid() and is_email(request.POST.get("username")):
			print(request.POST.get("username"))
			user=User.objects.create(username=request.POST.get("username"), email=request.POST.get("username"))
			user.set_password(request.POST.get("password"))
			
			print("creando usuario")
			user.save()
			
	ctx={}
	return(HttpResponse(template.render(ctx,request)))
	
	

class RegistroUsuario(CreateView):
	model = User
	template_name = "registrar.html"
	form_class = RegistroForm
	success_url = reverse_lazy("login")

@login_required
def Bienvenido(request):	
	return render_to_response('bienvenido.html',{})


#def index(request):
	#return HttpResponse("aqui estoy en index del login")