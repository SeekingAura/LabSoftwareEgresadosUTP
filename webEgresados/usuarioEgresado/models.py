from django.contrib.auth.models import User
from django.db import models
from usuarioAdminEgresado import models as userAdminEgreModel


#class amigosEgresado(models.Model):
#	DNI=models.CharField(max_length=30)
#	amigoDNI=models.CharField(max_length=30)
	
class UsuariosEgresado(models.Model):
	userEgre=models.ForeignKey(userAdminEgreModel.UsuariosAdminEgresado)
	#password=User.password
	
	pais=models.CharField(max_length=30)
	direccionTrabajo=models.CharField(max_length=100)
	fechaNacimiento=models.DateField()
	genero=models.CharField(max_length=6)
	programa=models.CharField(max_length=100)
	ocupacion=models.CharField(max_length=100)
	#amigos=models.CharField(max_length=100)#models.ForeignKey(amigosEgresado)
	#los intereses serán por tabla pivote
	
	#models.IntegerField()
	#models.FloatField()
	
