from django.db import models

# Create your models here.
class UsuariosEgresado(models.Model):

	
	nombre=models.CharField(max_length=25)
	apellidos=models.CharField(max_length=50)
	departamento=models.CharField(max_length=30)
	ciudad=models.CharField(max_length=30)
	direccion=models.CharField(max_length=100)
	telefono=models.CharField(max_length=15)
	estadoCuenta=models.CharField(max_length=15)
	
	
	#models.IntegerField()
	#models.FloatField()