from django.contrib.auth.models import User
from django.db import models
from usuarioAdminEgresado import models as UserAdminEgreModel

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

class UsuariosEgresado(models.Model):
	userEgre=models.ForeignKey(UserAdminEgreModel.UsuariosAdminEgresado)
	
	pais=models.CharField(max_length=30, blank=True)
	direccionTrabajo=models.CharField(max_length=100, blank=True)
	fechaNacimiento=models.DateField(blank=True)
	genero=models.CharField(max_length=6, blank=True)
	programa=models.CharField(max_length=100)
	ocupacion=models.CharField(max_length=100, blank=True)
	
	
	
	
	#amigos=models.ForeignKey(amigosEgresado)
	#intereses=models.ForeignKey(interesesEgresado)
	#models.ForeignKey(amigosEgresado)
	#los intereses serán por tabla pivote
	
	#models.IntegerField()
	#models.FloatField()
	
class AmigosEgresado(models.Model):
	userEgre=models.ForeignKey(UsuariosEgresado)
	amigoDNI=models.CharField(max_length=30)
	estado=models.CharField(max_length=10)
	
	
class InteresesEgresado(models.Model):
	userEgre=models.ForeignKey(UsuariosEgresado)
	interesID=models.CharField(max_length=30, validators=[numeric_validator])
	