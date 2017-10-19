from django.contrib.auth.models import User
from django.db import models
from usuarioAdminEgresado import models as userAdminEgreModel
# Create your models here.
class UsuarioAdministrador(models.Model):
	userEgre=models.ForeignKey(userAdminEgreModel.UsuariosAdminEgresado)
