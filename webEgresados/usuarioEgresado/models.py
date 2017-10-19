from django.contrib.auth.models import User
from django.db import models
from usuarioAdminEgresado import models as UserAdminEgreModel



class UsuariosEgresado(models.Model):
	userEgre=models.ForeignKey(UserAdminEgreModel.UsuariosAdminEgresado)
	
	pais=models.CharField(max_length=30)
	direccionTrabajo=models.CharField(max_length=100)
	fechaNacimiento=models.DateField()
	genero=models.CharField(max_length=6)
	programa=models.CharField(max_length=100)
	ocupacion=models.CharField(max_length=100)
	
	
	
	
	#amigos=models.ForeignKey(amigosEgresado)
	#intereses=models.ForeignKey(interesesEgresado)
	#models.ForeignKey(amigosEgresado)
	#los intereses serán por tabla pivote
	
	#models.IntegerField()
	#models.FloatField()
	
class AmigosEgresado(models.Model):
	DNI=models.CharField(max_length=30)
	amigoDNI=models.CharField(max_length=30)
	estado=models.CharField(max_length=10)
	userEgre=models.ForeignKey(UsuariosEgresado)
	
class InteresesEgresado(models.Model):
	DNI=models.CharField(max_length=30)
	interesID=models.CharField(max_length=30)
	userEgre=models.ForeignKey(UsuariosEgresado)