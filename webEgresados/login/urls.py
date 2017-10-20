from django.conf.urls import url
from .views import *
#from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
	url(r'^registrar', registro, name="registrar"),
	#url(r'^registrar/(?P<type>\w+)/$', registro, name="registrar"),
	url(r'^bienvenido', Bienvenido, name="bienvenido"),
]