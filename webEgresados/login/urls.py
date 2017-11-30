from django.conf.urls import url
from .views import Bienvenido, login_view, logout_view, registro, loginSudo_view, indexSudo_view, interesesTodosSudo_view, interesEliminarSudo_view, interesCrearSudo_view, solicitudesSudo_view, aceptarSoliSudo_view, rechazarSoliSudo_view

urlpatterns = [
	url(r'^bienvenido', Bienvenido, name="bienvenido"),
	url(r'^registrar/(?P<type>\w+)/$', registro, name="registrar"),
	url(r'^logout/', logout_view, name='logout'),
	url(r'^login', login_view, name="login"),
	url(r'^sudo/login', loginSudo_view, name="sudoLogin"),
	url(r'^sudo/index', indexSudo_view, name="sudoIndex"),
	url(r'^sudo/interescrear', interesCrearSudo_view, name="sudoInteresCrear"),
	url(r'^sudo/interesesver', interesesTodosSudo_view, name="sudoInteresesVer"),
	url(r'^sudo/intereseliminar/(?P<idInteres>\w+)/$', interesEliminarSudo_view, name="sudoInteresEliminar"),
	url(r'^sudo/solicitudes', solicitudesSudo_view, name="sudoSolicitudes"),
	url(r'^sudo/aceptarsolicitud/(?P<DNI>\w+)/$', aceptarSoliSudo_view, name="sudoAceptarSoli"),
	url(r'^sudo/rechazarsolicitud/(?P<DNI>\w+)/$', rechazarSoliSudo_view, name="sudoRechazarSoli"),
	
	
	
]