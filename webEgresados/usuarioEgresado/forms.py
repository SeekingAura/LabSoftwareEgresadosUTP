from django import forms
from django.contrib.auth.models import User
from usuarioAdminEgresado.models import UsuariosAdminEgresado, Pais, Departamento
from usuarioAdministrador.models import intereses

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
		

def departamentoValidator(paisValue, departamentoValue):
	resultDepartamento=Departamento.objects.get(departamentoNombre=departamentoValue)
	resultPais=Pais.objects.get(paisNombre=paisValue)
	if(resultDepartamento.idPais_id!=resultPais.id):
		return False
	return True

		
#query get values
def getPaises():
	templist=Pais.objects.all().values_list('paisNombre')
	result=[]
	for i in templist:
		tuple=[]
		tuple.append(i[0])
		tuple.append(i[0].title())
		result.append(tuple)
	result=sorted(result)
	
	return result

def getDepartamentos():
	templist=Departamento.objects.all().values_list('departamentoNombre')
	result=[]
	for i in templist:
		tuple=[]
		tuple.append(i[0])#.replace(" ", "_")
		tuple.append(i[0].title())
		result.append(tuple)
	
	result=sorted(result)
	result.insert(0, [None, "Seleccione Departamento"])
	return result

def getIntereses():
	templist=intereses.objects.all().values_list('titulo')
	result=[]
	for i in templist:
		tuple=[]
		tuple.append(i[0])
		tuple.append(i[0].title())
		result.append(tuple)
	return sorted(result)
	
def getDate():
	return [x for x in range(date.today().year-100,date.today().year)]
def getYears():
	actual=date.today().year
	result=[[None, "Seleccione año"]]
	for i in range(100):
		temp=[int(actual-i), str(actual-i)]
		result.append(temp)
	return result


	
class primerLogin_Form(forms.Form):
	
	pais=forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','placeholder':'Pais',
		'required':'true','maxlength':'32'}),required=True, 
		validators=[], choices=getPaises(),label="Pais", )
	departamento=forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','placeholder':'Departamento',
		'required':'true','maxlength':'32'}), required=True,
		validators=[], choices=getDepartamentos(),label="Departamento")
	
	intereses = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control','placeholder':'Intereses',
		'maxlength':'32'}),required=False, help_text="Estos intereses se usarán para filtrarle noticias que le sean de su interés",choices=getIntereses(), label="Intereses",validators=[])
	
	
	
	fechaNacimiento= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Fecha de nacimiento',
		'required':'true'}), required=True, label='Fecha de nacimiento')

	graduacion= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'año de graduación',
		'required':'true'}), required=True, label='año de graduación')
	
	genero=forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-control','placeholder':'Genero',
		'required':'true', 'maxlength':'32',}), choices=[["masculino", "Masculino"], ["femenino", "Femenino"]], required=True, validators=[],  label="Genero")
	
	direccionResidencia=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Dirección de residencia',
		'maxlength':'32',}), required=False, validators=[],  label="Dirección de residencia")
	direccionTrabajo=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Dirección de trabajo',
		'maxlength':'32',}), required=False, validators=[],  label="Dirección de Trabajo")
	ocupacionActual=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ocupación Actual',
		'maxlength':'32',}), required=False, validators=[],  label="Ocupación actual")
	telefono=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Telefono',
		'maxlength':'32',}), required=False, validators=[numeric_validator],  label="Telefono")
	privacidad=forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-control','placeholder':'Acceso a mi información',
		'required':'true', 'maxlength':'32',}), choices=[["publico","Publico"], ["amigos de amigos","Amigos de amigos (tus amigos están incluidos)"], ["amigos","Amigos"],["privado","Privado"]], initial="publico", required=True, validators=[],  label="Acceso a mi información")
	
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32', 'required':'true'}), label="Contraseña")
	passwordConfimation=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'repita contraseña','maxlength':'32', 'required':'true'}),validators=[validate_password], help_text=password_validators_help_text_html(), label="Confimar contraseña")

	def clean(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordConfimation')
		print("cleaned password1={}, password2={}".format(password1, password2))
		if password1 != password2 and password2 is not None:
			raise forms.ValidationError(('las contraseñas no coinciden'), code='invalid') 
		#else:
		#	 self.full_clean()
		return password2

class editarPerfil_Form(forms.Form):
	intereses = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control','placeholder':'Intereses',
		'maxlength':'32'}),required=False, help_text="Estos intereses se usarán para filtrarle noticias que le sean de su interés",choices=getIntereses(), label="Intereses",validators=[])
		
	direccionResidencia=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Dirección de residencia',
		'maxlength':'32',}), required=False, validators=[],  label="Dirección de residencia")
	direccionTrabajo=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Dirección de trabajo',
		'maxlength':'32',}), required=False, validators=[],  label="Dirección de Trabajo")
	ocupacionActual=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ocupación Actual',
		'maxlength':'32',}), required=False, validators=[],  label="Ocupación actual")
	telefono=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Telefono',
		'maxlength':'32',}), required=False, validators=[numeric_validator],  label="Telefono")
	privacidad=forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-control','placeholder':'Acceso a mi información',
		'required':'true', 'maxlength':'32',}), choices=[["publico","Publico"], ["amigos de amigos","Amigos de amigos (tus amigos están incluidos)"], ["amigos","Amigos"],["privado","Privado"]], initial="publico", validators=[],  label="Acceso a mi información")
	foto=forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control','placeholder':'Foto', 'id' : 'input-file'}),required=False, label="Foto")
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'contraseña','maxlength':'32'}), required=False, label="Contraseña")
	passwordConfimation=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'repita contraseña','maxlength':'32'}), required=False, validators=[validate_password], help_text=password_validators_help_text_html(), label="Confimar contraseña")
	
	def clean(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('passwordConfimation')
		if password1 != password2 and password2 is not None:
			raise forms.ValidationError(('las contraseñas no coinciden'), code='invalid') 
		#else:
		#	 self.full_clean()
		print(self.cleaned_data)
		return password2