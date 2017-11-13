from django.contrib import admin
from .models import UsuarioEgresado, InteresesEgresado, AmigosEgresado
admin.site.register (UsuarioEgresado)

@admin.register(InteresesEgresado)
class InteresesEgresado_Admin(admin.ModelAdmin):
	list_display = ("userEgre", "interes", )
	list_filter = ("userEgre", "interes",)

@admin.register(AmigosEgresado)
class AmigosEgresado_Admin(admin.ModelAdmin):
	list_display = ("userEgre", "amigoDNI", "estado",)
	list_filter = ("userEgre", "amigoDNI", "estado",)
# Register your models here.
