
from django.contrib import admin
from .models import UsuariosAdminEgresado, Pais
admin.site.register (UsuariosAdminEgresado)
# Register your models here.


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
	list_display = ("id", "paisNombre", )
	list_filter = ("id", "paisNombre", )