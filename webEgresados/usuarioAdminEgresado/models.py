from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

#def validate_DNI(value):
import re
from django.core.exceptions import ValidationError

def numeric_validator(value):
	result=re.match('[0-9]*', str(value))
	#print("el valor de value[0] es %s -" % (value[0]))
	if result is not None:	
		if len(result.group(0))!=len(str(value)):
			raise ValidationError('este campo debe ser solamente númerico')
	else:
		raise ValidationError('este campo debe ser solamente númerico')

# Create your models here.


class Pais(models.Model):
	paisNombre=models.CharField(max_length=30)

class Departamento(models.Model):
	idPais=models.ForeignKey(Pais)
	departamentoNombre=models.CharField(max_length=60)
	

class UsuariosAdminEgresado(models.Model):
	user=models.ForeignKey(User)
	DNI=models.CharField(max_length=30, primary_key=True, validators=[numeric_validator])
	departamento=models.CharField(max_length=30, blank=True)
	ciudad=models.CharField(max_length=30, blank=True)
	direccion=models.CharField(max_length=100, blank=True)
	telefono=models.CharField(max_length=15, validators=[numeric_validator], blank=True)
	estadoCuenta=models.CharField(max_length=15, choices=[("activada", "Activada"), ("pendiente", "Pendiente"), ("cerrada", "Cerrada")])
	#override
	def __str__ (self):
		return str(self.DNI)