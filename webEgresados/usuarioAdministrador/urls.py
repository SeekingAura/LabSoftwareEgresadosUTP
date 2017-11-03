from django.conf.urls import url
from .views import index, aceptarSoli_view, rechazarSoli_view

urlpatterns = [
	url(r'^index', index, name="index"),
	url(r'^aceptarsolicitud/(?P<DNI>\w+)/$', aceptarSoli_view, name="aceptarSoli"),
	url(r'^rechazarsolicitud/(?P<DNI>\w+)/$', rechazarSoli_view, name="rechazarSoli"),
	
	
	
]