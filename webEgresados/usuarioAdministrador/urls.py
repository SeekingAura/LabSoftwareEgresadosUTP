from django.conf.urls import url
from .views import solicitudes_view, aceptarSoli_view, rechazarSoli_view, crearNoticias_view

urlpatterns = [
	url(r'^solicitudes', solicitudes_view, name="index"),#por ahora este será el index, puede que cambie
	url(r'^aceptarsolicitud/(?P<DNI>\w+)/$', aceptarSoli_view, name="aceptarSoli"),
	url(r'^rechazarsolicitud/(?P<DNI>\w+)/$', rechazarSoli_view, name="rechazarSoli"),
	url(r'^crearnoticia', crearNoticias_view, name="crearNoticia"),
	
	
	
]