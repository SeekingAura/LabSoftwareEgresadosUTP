from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required


class RegistroUsuario(CreateView):
	model = User
	template_name = "login/templates/registrar.html"
	form_class = RegistroForm
	success_url = reverse_lazy("usuario:bienvenido")

@login_required
def Bienvenido(request):	
	return render_to_response('bienvenido.html',{})


#def index(request):
    #return HttpResponse("aqui estoy en index del login")