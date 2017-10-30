"""webEgresados URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login, password_reset 
from django.contrib.auth.views import password_reset_done, password_reset_confirm, password_reset_complete
from login.views import index

#This is for test url without views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', index, name="index"),
	url(r'^usuario/', include('login.urls', namespace="usuario")),
    #url(r'^logout/', logout_then_login, name='logout'),
	url(r'^reset/password_reset', password_reset, {'template_name':'password_reset_form.html', 'email_template_name':'password_reset_email.html'}, name='password_reset'),
    url(r'^reset/password_reset_done',password_reset_done,{'template_name':'password_reset_done.html'},name="password_reset_done"),
    #otro proceso de reset
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done', password_reset_complete, {'template_name':'password_reset_complete.html'}, name='password_reset_complete'),

    #This urls will be fort test
    url(r'^inicio', TemplateView.as_view(template_name="egresados/main.html"), name="egresadosInicio" ),
]
