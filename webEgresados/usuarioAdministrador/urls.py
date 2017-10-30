from django.conf.urls import url
from .views import index

urlpatterns = [
	url(r'^index', index, name="index"),
	#url(r'^registrar/(?P<type>\w+)/$', registro, name="registrar"),
	#url(r'^login', login_view, name="login"),
	#url(r'^logout/', logout_view, name='logout'),
	
	
]