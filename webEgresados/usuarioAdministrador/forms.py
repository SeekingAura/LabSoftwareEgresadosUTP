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


class crearNoticia_Form(forms.Form):
	titulo=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo', 'maxlength':'100',}), required=True, validators=[noticiaAlreadyExist_validator],  label="Titulo")
	contenido=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Contenido', 'maxlength':'500',}), required=True, validators=[],  label="Contenido")
	intereses = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control','placeholder':'Intereses', 'maxlength':'32'}),required=False, help_text="Estos intereses se usarán para que se filtre noticias que sean del interes de los egresados", choices=getIntereses(), label="Intereses",validators=[])
	
class modificarNoticia_Form(forms.Form):
	titulo=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo', 'maxlength':'100',}), required=True, validators=[],  label="Titulo")
	contenido=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Contenido', 'maxlength':'500',}), required=True, validators=[],  label="Contenido")
	intereses = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control','placeholder':'Intereses', 'maxlength':'32'}),required=False, help_text="Estos intereses se usarán para que se filtre noticias que sean del interes de los egresados", choices=getIntereses(), label="Intereses",validators=[])
	
		
	

	