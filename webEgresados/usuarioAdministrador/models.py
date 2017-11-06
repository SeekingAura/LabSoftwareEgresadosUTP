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