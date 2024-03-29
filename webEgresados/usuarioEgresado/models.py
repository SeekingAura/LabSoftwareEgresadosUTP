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

		


class ProgramaAcademico(models.Model):
	nombre=models.CharField(max_length=300)
	estado=models.CharField(max_length=50, choices=[["activo","Activo"], ["desactivado","Desactivado"]])
	class Meta:
		verbose_name="Programa Academico"
		verbose_name_plural = "Programas Academicos"

def getProgramas():
	programaslist=[]
	try:
		programas=ProgramaAcademico.objects.all()
	except:
		return [("ingenieria de sistemas", "Ingenieria de sistemas"), ("ingenieria industrial", "Ingenieria industrial"), ("ingenieria Mecanica", "Ingenieria Mecanica")]
	for i in programas:
		programaslist.append([i.nombre, i.nombre])
	
	#sorted(tempValues, key=attrgetter('nombre'), reverse=True)
	return sorted(programaslist)
		
class GraduadosPersonas(models.Model):
	DNI=models.CharField(max_length=100)
	first_name=models.CharField(max_length=300)
	last_name=models.CharField(max_length=300)
	promoteAge=models.IntegerField()
	class Meta:
		verbose_name="Graduado Persona"
		verbose_name_plural = "Graduados Personas"
	def __str__ (self):
		return "DNI - "+str(self.DNI)+" - "+str(self.first_name)+str(self.last_name)

class Graduados(models.Model):
	gradPersonas=models.ForeignKey(GraduadosPersonas)
	programa=models.CharField(max_length=100, choices=getProgramas())
	class Meta:
		verbose_name="Graduado"
		verbose_name_plural = "Graduados"
	def __str__ (self):
		return str(self.gradPersonas)
	
	
class UsuarioEgresado(models.Model):
	userAdminEgre=models.ForeignKey(UserAdminEgreModel.UsuariosAdminEgresado)
	direccionTrabajo=models.CharField(max_length=100, blank=True)
	fechaNacimiento=models.DateField(blank=True, null=True)
	genero=models.CharField(max_length=10, choices=[["masculino","Masculino"], ["femenino","Femenino"], ["ninguno","N/A"]], blank=True)
	
	
	foto=models.ImageField(upload_to = "photo", default = 'photo/None/no-img.jpg',blank=True, null=True)
	programa=models.CharField(max_length=100, choices=getProgramas())
	promoteAge=models.IntegerField(blank=True, null=True)
	privacidad=models.CharField(max_length=10, choices=[["publico","Publico"], ["amigos de amigos","Amigos de amigos (tus amigos están incluidos)"], ["amigos","Amigos"],["privado","Privado"]], blank=True)
	ocupacionActual=models.CharField(max_length=100, blank=True)
	def __str__ (self):
		return "Egresado - "+str(self.userAdminEgre.user.first_name)+" - "+str(self.userAdminEgre.user)
	
	class Meta:
		verbose_name="Usuario Egresado"
		verbose_name_plural = "Usuarios Egresados"
	
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
	interes=models.ForeignKey(interesesModel)
	class Meta:
		verbose_name = "Interes de Egresado"
		verbose_name_plural = "Intereses de egresados"
	
	def __str__ (self):
		return str(self.userEgre)+" - "+str((self.interes))
	
