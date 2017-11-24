from django.conf.urls import url
from .views import Bienvenido, login_view, logout_view, registro, loginSudo_view, indexSudo_view

urlpatterns = [
	url(r'^bienvenido', Bienvenido, name="bienvenido"),
	url(r'^registrar/(?P<type>\w+)/$', registro, name="registrar"),
	url(r'^login', login_view, name="login"),
	url(r'^sudo/login', loginSudo_view, name="sudoLogin"),
	url(r'^sudo/index', indexSudo_view, name="sudoIndex"),
	url(r'^logout/', logout_view, name='logout'),
	
	
]