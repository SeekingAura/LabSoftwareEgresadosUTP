from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class registroAdmin(UserCreationForm):
	#Otros atributos para el usuairo
	class Meta:
		model = User
		fields = [
				'username',
				'first_name',
				'last_name',
				'email',
			]

		labels = {
				'username': 'Nombre de usuario',
				'first_name':'Nombre',
				'last_name':'Apellidos',
				'email':'Correo',		}

class registroEgresado(forms.Form):
	nombres = forms.CharField(max_length=50, label="Nombres")
	apellidos = forms.CharField(max_length=50, label="Apellidos")
	correo = forms.EmailField()
	programa = forms.CharField(max_length=50, label="Programa academico")