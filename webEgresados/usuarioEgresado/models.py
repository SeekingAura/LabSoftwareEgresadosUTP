from django.contrib.auth.models import User
from django.db import models

class UsuariosEgresado(models.Model):
	user=models.ForeignKey(User)
	
	#password=User.password
	
	pais=models.CharField(max_length=30)
	direccionTrabajo=models.CharField(max_length=100)
	fechaNacimiento=models.DateField()
	genero=models.CharField(max_length=6)
	programa=models.CharField(max_length=100)
	ocupacion=models.CharField(max_length=100)
	#los intereses serán por tabla pivote
	
	#models.IntegerField()
	#models.FloatField()