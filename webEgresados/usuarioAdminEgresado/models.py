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

#información de los paises y sus departamentos https://github.com/ponceelrelajado/paises_estados_del_mundo
class Pais(models.Model):
	paisNombre=models.CharField(max_length=30)
	
	class Meta:
		verbose_name = "Pais"
		verbose_name_plural = "Paises"
	
	def __str__(self):
		return self.paisNombre

class Departamento(models.Model):
	idPais=models.ForeignKey(Pais)
	departamentoNombre=models.CharField(max_length=60)
	class Meta:
		verbose_name = "Departamento"
		verbose_name_plural = "Departamentos"
	
	def __str__(self):
		return self.departamentoNombre


class UsuariosAdminEgresado(models.Model):
	user=models.ForeignKey(User)
	DNI=models.CharField(max_length=30, primary_key=True, validators=[numeric_validator])
	departamento=models.CharField(max_length=100, blank=True)
	pais=models.CharField(max_length=100, blank=True)
	ciudad=models.CharField(max_length=30, blank=True)
	direccionResidencia=models.CharField(max_length=100, blank=True)
	telefono=models.CharField(max_length=15, validators=[numeric_validator], blank=True)
	estadoCuenta=models.CharField(max_length=15, choices=[("activada", "Activada"),("pendiente", "Pendiente"), ("cerrada", "Cerrada"), ("rechazada", "Rechazar")])
	#override
	class Meta:
		verbose_name = "Usuario Administrador Egresado"
		verbose_name_plural = "Usuarios Administradores Egresados"
	
	def __str__ (self):
		return str(self.user.first_name)+" - "+str(self.user)