from django import forms
from django.contrib.auth.models import User
from usuarioAdminEgresado.models import UsuariosAdminEgresado

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


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
		
def verify_StateAccount(username):
	user=None
	try:
		user=User.objects.get(username=username)
		user=UsuariosAdminEgresado.objects.get(user_id=user.id)
	except:
		user=None
	if(user is not None):
		if(user.estadoCuenta!="Activada"):
			raise ValidationError('Su cuenta no está activa, consulte con un admin sobre su asunto')
	else:
		raise ValidationError('Cuenta no encontrada')

		
class registroAdministrador(forms.Form):
	
	DNI=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'DNI',
		'required':'true','maxlength':'32', 'label':'Número de identificación'}), 
		validators=[numeric_validator, verify_alredyExistDNI])
	username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'correo electrónico',
		'required':'true', 'label':'Correo electrónico'}), validators=[verify_alredyExistEmail])
	first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombres',
		'required':'true', 'label':'Nombres', 'maxlength':'32',}))
	last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos',
		'required':'true', 'label':'Apellidos', 'maxlength':'32',}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32', 'required':'true'}))
	passwordConfimation=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'repita contraseña','maxlength':'32', 'required':'true'}))
		
		
	
	def clean(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordConfimation')
		if password1 != password2:
			raise forms.ValidationError(('las contraseñas no coinciden'), code='invalid') 
		#else:
		#	 self.full_clean()
		return password2
	
		
class registroEgresado(forms.Form):
	DNI=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'DNI',
		'required':'true','maxlength':'32', 'label':'Número de identificación'}), validators=[numeric_validator, verify_alredyExistDNI])
	username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'correo electrónico',
		'required':'true', 'label':'Correo electrónico'}), validators=[verify_alredyExistEmail])
	first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombres',
		'required':'true', 'label':'Nombres', 'maxlength':'32',}))
	last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos',
		'required':'true', 'label':'Apellidos', 'maxlength':'32',}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32', 'required':'true'}))
	passwordConfimation=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'repita contraseña','maxlength':'32', 'required':'true'}))
	programa = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'DNI',
		'required':'true','maxlength':'32', 'label':'Programa académico'}))
	
	def clean(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordConfimation')
		if password1 != password2:
			raise forms.ValidationError(('las contraseñas no coinciden'), code='invalid')
		return password2


class loginForm(forms.Form):
	username = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'correo electronico','required':'true'}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32', 'required':'true'}))
	def clean(self):
		username = str(self.cleaned_data.get('username')).lower()
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		
		if not user or not user.is_active:
			raise forms.ValidationError("Usuario o contraseña invalidos")
		elif(user):
			verify_StateAccount(username)
			
		return self.cleaned_data

	def login(self, request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		return user
		
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
