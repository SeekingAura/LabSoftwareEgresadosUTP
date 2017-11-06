from django.contrib import admin
from .models import UsuarioAdministrador, intereses

# Register your models here.
admin.site.register (UsuarioAdministrador)

@admin.register(intereses)
class interesesAdmin(admin.ModelAdmin):
	list_display = ("titulo", "description", )
	#list_filter = ("titulo", )