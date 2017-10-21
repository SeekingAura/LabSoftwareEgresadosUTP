from django.conf.urls import url
from django.contrib.auth.views import login
from .views import *
#from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
	#url(r'^registrar', registro, name="registrar"),
	url(r'^bienvenido', Bienvenido, name="bienvenido"),
	url(r'^registrar/(?P<type>\w+)/$', registro, name="registrar"),
	url(r'^login', login, {'template_name':'login.html'},name="login"),
]