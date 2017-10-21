from django import forms
from django.contrib.auth.models import User
from usuarioAdminEgresado.models import UsuariosAdminEgresado

from django.contrib.auth.forms import UserCreationForm



from django.forms import ModelForm
from django.core.validators import EmailValidator
import re
from django.core.exceptions import ValidationError

def numeric_validator(value):
	result=re.match('[0-9]*', str(value))
	if result is not None:	
		
		if len(result.group(0))!=len(str(value)):
			raise ValidationError('este campo debe ser solamente númerico')
	else:
		
		raise ValidationError('este campo debe ser solamente númerico')
		


		

def verify_alredyExistEmail(email):
	existe=False
	try:
		User.objects.get(username=email)
		existe=True
	except:
		existe=False
	if(existe):
		raise ValidationError('ya existe este email')

def verify_alredyExistDNI(DNI):
	existe=False
	try:
		UsuariosAdminEgresado.objects.get(DNI=DNI)
		
		existe=True
	except:
		existe=False
	if(existe):
		raise ValidationError('ya existe este DNI')
		
		
class registroAdministrador(forms.Form):
	
	DNI=forms.CharField(max_length=32, label="Número de identificación", validators=[numeric_validator, verify_alredyExistDNI], required=True)
	username = forms.EmailField(label="usuario (Email)",required=True, validators=[verify_alredyExistEmail])
	first_name=forms.CharField(max_length=32, label="Nombres", required=True)
	last_name=forms.CharField(max_length=32, label="Apellidos", required=True)
	password=forms.CharField(max_length=32, widget=forms.PasswordInput(), label="Contraseña", required=True)
	passwordConfimation=forms.CharField(max_length=32, widget=forms.PasswordInput(), label="Contraseña (Confirmación)", required=True)
		
		
	
	def clean(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordConfimation')
		if password1 != password2:
			raise forms.ValidationError(('las contraseñas no coinciden'), code='invalid') 
		return password2
	
		
class registroEgresado(forms.Form):
	DNI=forms.CharField(max_length=32, label="Número de identificación", validators=[numeric_validator, verify_alredyExistDNI], required=True)
	username = forms.EmailField(label="usuario (Email)",required=True, validators=[verify_alredyExistEmail])
	nombres=forms.CharField(max_length=32, label="Nombres", required=True)
	apellidos=forms.CharField(max_length=32, label="Apellidos", required=True)
	password=forms.CharField(max_length=32, widget=forms.PasswordInput(), label="Contraseña", required=True)
	passwordConfimation=forms.CharField(max_length=32, widget=forms.PasswordInput(), label="Contraseña (Confirmación)", required=True)
	programa = forms.CharField(max_length=50, label="Programa academico", required=True)
	
	def clean(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordConfimation')
		if password1 != password2:
			raise forms.ValidationError(('las contraseñas no coinciden'), code='invalid')
		return password2


"""
class RegistroForm(UserCreationForm):
	username = forms.EmailField(label=_("usuario (Email)"))
	#email = forms.EmailField(label=_("usuario (Email)"))

	class Meta:
		model = User
		fields = ["username"]
"""
	
"""
class RegistroForm(forms.Form):
	username=forms.CharField(max_length=30)
	first_name=forms.CharField(max_length=30)
	last_name=forms.CharField(max_length=30)
	email=forms.EmailField(max_length=30)
"""
"""
class RegistroForm(UserCreationForm):
	#Otros atributos para el usuario
	
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
				'last_name':'Apellido',
				'email':'Correo',}
"""			
