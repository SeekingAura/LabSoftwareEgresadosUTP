
from django.contrib import admin
from .models import UsuariosAdminEgresado, Pais, Departamento

# Register your models here.

admin.site.register (UsuariosAdminEgresado)
@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
	list_display = ("id", "paisNombre", )
	list_filter = ("paisNombre", )
	
@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
	list_display = ("id", "departamentoNombre", "idPais", )
	list_filter = ("idPais",)
	
	