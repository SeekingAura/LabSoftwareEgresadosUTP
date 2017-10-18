from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

#def validate_DNI(value):
import re
from django.core.exceptions import ValidationError

def numeric_validator(value):
	result=re.match('[0-9]*', str(value))
	print("el valor de value[0] es %s -" % (value[0]))
	if result is not None:	
		if len(result.group(0))!=len(str(value)):
			raise ValidationError('el valor {} No es un número. Un DNI debe ser unicamente números'.format(value))
	else:
		raise ValidationError('el valor {} No es un número. Un DNI debe ser unicamente números'.format(value))

# Create your models here.

class UsuariosAdminEgresado(models.Model):
	user=models.ForeignKey(User)
	DNI=models.CharField(max_length=30, primary_key=True, validators=[numeric_validator])
	departamento=models.CharField(max_length=30)
	ciudad=models.CharField(max_length=30)
	direccion=models.CharField(max_length=100)
	telefono=models.CharField(max_length=15)
	estadoCuenta=models.CharField(max_length=15)
	#override
	#def __str__ (self):
	#	return self.nombre + " " + self.apellidos