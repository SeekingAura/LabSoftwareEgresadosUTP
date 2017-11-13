from django.contrib.auth.models import User
from django.db import models
from usuarioAdminEgresado import models as userAdminEgreModel
# Create your models here.
class UsuarioAdministrador(models.Model):
	userAdminEgre=models.ForeignKey(userAdminEgreModel.UsuariosAdminEgresado)
	def __str__ (self):
		return str(self.userAdminEgre)


class intereses(models.Model):
	titulo=models.CharField(max_length=50, primary_key=True, validators=[])
	description=models.CharField(max_length=300, validators=[])
	def __str__ (self):
		return str(self.titulo)
		
	class Meta:
		verbose_name="Interes"
		verbose_name_plural = "Intereses"
		
class noticias(models.Model):
	titulo=models.CharField(max_length=100, primary_key=True, validators=[])
	contenido=models.TextField(max_length=500, validators=[])
	creador=models.ForeignKey(UsuarioAdministrador)
	class Meta:
		verbose_name = "Noticia"
		verbose_name_plural = "Noticias"
	
	def __str__ (self):
		return str(self.titulo)

class noticiasIntereses(models.Model):
	noticia=models.ForeignKey(noticias)
	interes=models.ForeignKey(intereses)
	class Meta:
		verbose_name = "Intereses de noticia"
		verbose_name_plural = "Intereses de noticias"
	
	def __str__ (self):
		return str(self.noticia)+" - "+str(self.interes)