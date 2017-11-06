from django.contrib import admin
from .models import UsuarioEgresado, InteresesEgresado
admin.site.register (UsuarioEgresado)

@admin.register(InteresesEgresado)
class interesesAdmin(admin.ModelAdmin):
	list_display = ("userEgre", "interes", )
	list_filter = ("userEgre", )
# Register your models here.
