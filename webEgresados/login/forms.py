from django import forms
from django.contrib.auth.models import User
from usuarioAdminEgresado.models import UsuariosAdminEgresado

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


from django.forms import ModelForm
from django.core.validators import EmailValidator
import re
from django.core.exceptions import ValidationError
from django.contrib import messages


def numeric_validator(value):
	result=re.match('[0-9]*', str(value))
	if result is not None:	
		
		if len(result.group(0))!=len(str(value)):
			
			raise ValidationError('este campo debe ser solamente númerico')
	else:
		
		raise ValidationError('este campo debe ser solamente númerico')
		
def name_validator(value):
	guion=False
	for i in str(value):
		if i=="-":
			if(guion):
				raise ValidationError('Un nombre no puede contener varios guiones seguidos')
			guion=True
		else:
			guion=False
	valueInput=value.replace("-", "")
	espacio=False
	for i in str(valueInput):
		if i==" ":
			if(espacio):
				raise ValidationError('Un nombre debe estar separado 1 solo espacio')
			espacio=True
		else:
			espacio=False
	valueInput=value.replace(" ", "")
	testValue=""
	for enum,i in enumerate(str(valueInput)):
		if(i==" "):
			if(testValue.isalpha()):
				testValue=""
			else:
				raise ValidationError('este campo debe ser solamente alfabetico')
		if(enum==len(str(valueInput))-1):
			testValue+=i
			if(testValue.isalpha()):
				testValue=""
			else:
				raise ValidationError('este campo debe ser solamente alfabetico')
		else:
			testValue+=i
	
	
	
	
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
		if(user.estadoCuenta!="activada"):
			raise ValidationError('Su cuenta no está activa, consulte con un admin sobre su asunto')
	else:
		raise ValidationError('Cuenta no encontrada')

		
class registroAdministrador(forms.Form):
	
	DNI=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'DNI',
		'required':'true','maxlength':'32'}), 
		validators=[numeric_validator, verify_alredyExistDNI], label="Número de identificación")
	username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'correo electrónico',
		'required':'true'}), validators=[verify_alredyExistEmail], label="Correo electrónico")
	first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombres',
		'required':'true', 'maxlength':'32',}), validators=[name_validator], label="Nombres")
	last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos',
		'required':'true', 'maxlength':'32',}), validators=[name_validator],  label="Apellidos")
	
	
	
	"""
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32', 'required':'true'}), label="Contraseña")
	passwordConfimation=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'repita contraseña','maxlength':'32', 'required':'true'}),label="Confimar contraseña")

	def clean(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordConfimation')
		if password1 != password2:
			raise forms.ValidationError(('las contraseñas no coinciden'), code='invalid') 
		#else:
		#	 self.full_clean()
		return password2
	"""

def getProgramas():
		return [("", "Seleccione programa"), ("ingenieria de sistemas", "Ingenieria de sistemas"), ("ingenieria industrial", "Ingenieria industrial"), ("ingenieria Mecanica", "Ingenieria Mecanica")]
	
class registroEgresado(forms.Form):
	DNI=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'DNI',
		'required':'true','maxlength':'32'}), validators=[numeric_validator, verify_alredyExistDNI], label="Número de identificación")
	username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'correo electrónico',
		'required':'true'}), validators=[verify_alredyExistEmail], label="Correo electrónico")
	first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombres',
		'required':'true', 'maxlength':'32',}), validators=[name_validator], label="Nombres")
	last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos',
		'required':'true', 'maxlength':'32',}), validators=[name_validator], label="Apellidos")
	
	programa = forms.CharField(widget=forms.Select(attrs={'class':'form-control','placeholder':'DNI',
		'required':'true','maxlength':'32'}, choices=getProgramas()), label="Programa Academico")
	def clean(self):
		if(not self.is_valid()):
			raise forms.ValidationError("Hay errores en los campos")
	"""
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32', 'required':'true'}), label="Contraseña")
	passwordConfimation=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'repita contraseña','maxlength':'32', 'required':'true'}), label="Confirmar contraseña")
	
	
	def clean(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordConfimation')
		if password1 != password2:
			raise forms.ValidationError(('las contraseñas no coinciden'), code='invalid')
		return password2
	"""

class loginForm(forms.Form):
	username = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'correo electronico','required':'true'}), label="Correo electrónico")
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32', 'required':'true'}), label="Contraseña")
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

class loginSudo_Form(forms.Form):
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32', 'required':'true'}), label="Contraseña")
	def clean(self):
		password = self.cleaned_data.get('password')
		user = authenticate(username="sudo", password=password)
		
		if not user or not user.is_active:
			raise forms.ValidationError("Usuario o contraseña invalidos")
			
		return self.cleaned_data

	def login(self, request):
		password = self.cleaned_data.get('password')
		user = authenticate(username="sudo", password=password)
		return user

class crearInteres_Form(forms.Form):
	titulo=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo', 'maxlength':'100',}), required=True, validators=[],  label="Titulo")
	description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Contenido', 'maxlength':'500',}), required=True, validators=[],  label="Contenido")

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
