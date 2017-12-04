from django.contrib import admin
from .models import UsuarioEgresado, InteresesEgresado, AmigosEgresado, ProgramaAcademico, GraduadosPersonas, Graduados
admin.site.register (UsuarioEgresado)

@admin.register(InteresesEgresado)
class InteresesEgresado_Admin(admin.ModelAdmin):
	list_display = ("userEgre", "interes", )
	list_filter = ("userEgre", "interes",)

@admin.register(AmigosEgresado)
class AmigosEgresado_Admin(admin.ModelAdmin):
	list_display = ("userEgre", "amigoDNI", "estado",)
	list_filter = ("userEgre", "amigoDNI", "estado",)

admin.site.register(ProgramaAcademico)
admin.site.register(GraduadosPersonas)
admin.site.register(Graduados)
