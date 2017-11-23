from django.conf.urls import url
from .views import index_view, primerLogin_view, verNoticias_view, editarPerfil_view

urlpatterns = [
	url(r'^index', index_view, name="index"),
	url(r'^primerlogin', primerLogin_view, name="primerLogin"),
	url(r'^noticias', verNoticias_view, name="noticiasTodas"),
	url(r'^editarPerfil', editarPerfil_view, name="editarPerfil"),
	#url(r'^registrar/(?P<type>\w+)/$', registro, name="registrar"),
	#url(r'^login', login_view, name="login"),
	#url(r'^logout/', logout_view, name='logout'),
	
	
]