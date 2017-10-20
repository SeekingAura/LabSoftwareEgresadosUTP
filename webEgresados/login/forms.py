from django import forms
from django.contrib.auth.models import User


from django.contrib.auth.forms import UserCreationForm


from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm


class RegistroForm(ModelForm):
	class Meta:
		model=User
		fields=["username", "password"]



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
