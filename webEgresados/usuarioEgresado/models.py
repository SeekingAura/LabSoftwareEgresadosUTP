from django.contrib.auth.models import User
from django.db import models
from usuarioAdminEgresado import models as UserAdminEgreModel
from usuarioAdministrador.models import intereses as interesesModel
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

		
def getProgramas():
		return [("ingenieria de sistemas", "Ingenieria de sistemas"), ("ingenieria industrial", "Ingenieria industrial"), ("ingenieria Mecanica", "Ingenieria Mecanica")]
		
class UsuarioEgresado(models.Model):
	userAdminEgre=models.ForeignKey(UserAdminEgreModel.UsuariosAdminEgresado)
	direccionTrabajo=models.CharField(max_length=100, blank=True)
	fechaNacimiento=models.DateField(blank=True, null=True)
	genero=models.CharField(max_length=10, choices=[["masculino","Masculino"], ["femenino","Femenino"], ["ninguno","N/A"]], blank=True)
	
	
	
	programa=models.CharField(max_length=100, choices=getProgramas())
	promoteAge=models.DateField(blank=True, null=True)
	privacidad=models.CharField(max_length=10, choices=[["publico","Publico"], ["amigos de amigos","Amigos de amigos (tus amigos están incluidos)"], ["amigos","Amigos"],["privado","Privado"]], blank=True)
	ocupacion=models.CharField(max_length=100, blank=True)
	def __str__ (self):
		return str(self.userAdminEgre)
	
	
	
	#amigos=models.ForeignKey(amigosEgresado)
	#intereses=models.ForeignKey(interesesEgresado)
	#models.ForeignKey(amigosEgresado)
	#los intereses serán por tabla pivote
	
	#models.IntegerField()
	#models.FloatField()

class AmigosEgresado(models.Model):
	userEgre=models.ForeignKey(UsuarioEgresado)
	amigoDNI=models.CharField(max_length=30)
	estado=models.CharField(max_length=10)
	
	
class InteresesEgresado(models.Model):
	userEgre=models.ForeignKey(UsuarioEgresado)
	interes=models.CharField(max_length=30, validators=[numeric_validator])
	