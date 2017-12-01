from django import forms
from django.contrib.auth.models import User
from usuarioAdminEgresado.models import UsuariosAdminEgresado, Pais, Departamento
from usuarioAdministrador.models import intereses, noticias

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html


from django.forms import ModelForm
from django.core.validators import EmailValidator
import re
from django.core.exceptions import ValidationError
from django.contrib import messages


from datetime import date

#validators
def numeric_validator(value):
	result=re.match('[0-9]*', str(value))
	if result is not None:	
		
		if len(result.group(0))!=len(str(value)):
			
			raise ValidationError('este campo debe ser solamente númerico')
	else:
		
		raise ValidationError('este campo debe ser solamente númerico')
	
def noticiaAlreadyExist_validator(value):
	value=value.lower()
	
	temp=noticias.objects.all().values_list('titulo')
	for i in temp:
		if str(i[0]).lower()==value:
			raise ValidationError('Ya existe una noticia con dicho nombre')
	
	
		

def getIntereses():
	templist=intereses.objects.all().values_list('titulo')
	result=[]
	for i in templist:
		tuple=[]
		tuple.append(i[0])
		tuple.append(i[0].title())
		result.append(tuple)
	return sorted(result)	

def getDepartamentos():
	paisLugar=Pais.objects.get(paisNombre="Colombia")
	templist=Departamento.objects.all().filter(idPais=paisLugar.id).values_list('departamentoNombre')
	result=[]
	for i in templist:
		tuple=[]
		tuple.append(i[0])#.replace(" ", "_")
		tuple.append(i[0].title())
		result.append(tuple)
	
	result=sorted(result)
	result.insert(0, [None, "Seleccione Departamento"])
	return result

class crearNoticia_Form(forms.Form):
	titulo=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo', 'maxlength':'100',}), required=True, validators=[noticiaAlreadyExist_validator],  label="Titulo")
	contenido=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Contenido', 'maxlength':'500',}), required=True, validators=[],  label="Contenido")
	intereses = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control','placeholder':'Intereses', 'maxlength':'32'}),required=False, help_text="Estos intereses se usarán para que se filtre noticias que sean del interes de los egresados", choices=getIntereses(), label="Intereses",validators=[])
	
class modificarNoticia_Form(forms.Form):
	titulo=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo', 'maxlength':'100',}), required=True, validators=[],  label="Titulo")
	contenido=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Contenido', 'maxlength':'500',}), required=True, validators=[],  label="Contenido")
	intereses = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control','placeholder':'Intereses', 'maxlength':'32'}),required=False, help_text="Estos intereses se usarán para que se filtre noticias que sean del interes de los egresados", choices=getIntereses(), label="Intereses",validators=[])
	
class primerLogin_Form(forms.Form):
	departamento=forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','placeholder':'Departamento',
		'required':'true','maxlength':'32'}), required=True,
		validators=[], choices=getDepartamentos(),label="Departamento")
	
	direccionResidencia=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Dirección de residencia',
		'maxlength':'32',}), required=False, validators=[],  label="Dirección de residencia")
	telefono=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Telefono',
		'maxlength':'32',}), required=False, validators=[numeric_validator],  label="Telefono")
	
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32', 'required':'true'}), label="Contraseña")
	passwordConfimation=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'repita contraseña','maxlength':'32', 'required':'true'}),validators=[validate_password], help_text=password_validators_help_text_html(), label="Confimar contraseña")

	def clean(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordConfimation')
		#print("cleaned password1={}, password2={}".format(password1, password2))
		if password1 != password2 and password2 is not None:
			raise forms.ValidationError(('las contraseñas no coinciden'), code='invalid') 
		#else:
		#	 self.full_clean()
		return password2
	
class editarPerfil_Form(forms.Form):
	
	direccionResidencia=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Dirección de residencia',
		'maxlength':'32',}), required=False, validators=[],  label="Dirección de residencia")
	telefono=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Telefono',
		'maxlength':'32',}), required=False, validators=[numeric_validator],  label="Telefono")
	
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32', 'required':'true'}), label="Contraseña")
	passwordConfimation=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'repita contraseña','maxlength':'32', 'required':'true'}),validators=[validate_password], help_text=password_validators_help_text_html(), label="Confimar contraseña")

	def clean(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordConfimation')
		#print("cleaned password1={}, password2={}".format(password1, password2))
		if password1 != password2 and password2 is not None:
			raise forms.ValidationError(('las contraseñas no coinciden'), code='invalid') 
		#else:
		#	 self.full_clean()
		return password2
	

	