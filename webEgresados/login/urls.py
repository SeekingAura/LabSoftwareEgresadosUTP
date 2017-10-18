from django.conf.urls import url
from .views import registro, Bienvenido
#from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
	url(r'^registrar/(?P<type>\w+)/$', registro, name="registrar"),
	url(r'^bienvenido', Bienvenido, name="bienvenido"),
]