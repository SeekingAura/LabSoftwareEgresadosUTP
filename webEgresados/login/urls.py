from django.conf.urls import url
from .views import RegistroUsuario, Bienvenido
#from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
	url(r'^registrar', RegistroUsuario.as_view(), name="registrar"),
	url(r'^bienvenido', Bienvenido, name="bienvenido"),
]