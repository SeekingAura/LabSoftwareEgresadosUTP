from django.contrib import admin
from .models import UsuarioAdministrador, intereses, noticias, noticiasIntereses

# Register your models here.
admin.site.register (UsuarioAdministrador)

@admin.register(intereses)
class intereses_Admin(admin.ModelAdmin):
	list_display = ("titulo", "description", )
	#list_filter = ("titulo", )

@admin.register(noticias)
class noticias_Admin(admin.ModelAdmin):
	list_display = ("titulo", "creador", )
	list_filter = ("creador", )

@admin.register(noticiasIntereses)
class noticiasIntereses_Admin(admin.ModelAdmin):
	list_display = ("noticia", "interes", )
	list_filter = ("interes", )
	

	