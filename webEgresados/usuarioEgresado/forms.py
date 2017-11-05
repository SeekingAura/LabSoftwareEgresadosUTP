from django import forms
from django.contrib.auth.models import User
from usuarioAdminEgresado.models import UsuariosAdminEgresado, Pais

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password


from django.forms import ModelForm
from django.core.validators import EmailValidator
import re
from django.core.exceptions import ValidationError
from django.contrib import messages

from datetime import date


def numeric_validator(value):
	result=re.match('[0-9]*', str(value))
	if result is not None:	
		
		if len(result.group(0))!=len(str(value)):
			
			raise ValidationError('este campo debe ser solamente númerico')
	else:
		
		raise ValidationError('este campo debe ser solamente númerico')
		

YEARS= [x for x in range(date.today().year-100,date.today().year)]
def paisCreator():
	temp=["pais1", "pais2", "pais3"]
	templist=Pais.objects.all().values_list('paisNombre')
	print(templist)
	result=[]
	for i in templist:
		tuple=[]
		tuple.append(i[0])
		tuple.append(i[0].title())
		result.append(tuple)
	
	return sorted(result)
		
class primerLogin_Form(forms.Form):
	
	pais=forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','placeholder':'Pais',
		'required':'true','maxlength':'32'}), 
		validators=[], choices=paisCreator(),label="pais")
	intereses = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'correo electrónico',
		'required':'true'}), validators=[], label="Intereses")
	
	fechaNacimiento= forms.DateField(widget=forms.SelectDateWidget(attrs={'class':'form-control','placeholder':'correo electrónico',
		'required':'true'},years=YEARS), label='Fecha de nacimiento', initial="1990-06-21")


	#fechaNacimiento=forms.DateField(widget=forms.SelectDateWidget(attrs={'class':'form-control','placeholder':'Nombres',
	#	'required':'true', 'maxlength':'32',}, empty_label=("Choose Year", "Choose Month", "Choose Day"),
    #), validators=[], label="Fecha de nacimiento")
	genero=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos',
		'required':'true', 'maxlength':'32',}), validators=[],  label="Genero")
	direccionResidencia=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos',
		'required':'true', 'maxlength':'32',}), validators=[],  label="Dirección de residencia")
	direccionTrabajo=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos',
		'required':'true', 'maxlength':'32',}), validators=[],  label="Dirección de Trabajo")
	ocupacionActual=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos',
		'required':'true', 'maxlength':'32',}), validators=[],  label="Ocupación actual")
	telefono=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos',
		'required':'true', 'maxlength':'32',}), validators=[numeric_validator],  label="Dirección de residencia")
	isPublico=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos',
		'required':'true', 'maxlength':'32',}), validators=[numeric_validator],  label="Dirección de residencia")
	
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
	