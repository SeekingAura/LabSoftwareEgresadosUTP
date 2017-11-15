from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.contrib.auth.models import User
from usuarioAdminEgresado.models import UsuariosAdminEgresado
from usuarioAdministrador.models import UsuarioAdministrador
from usuarioEgresado.models import UsuarioEgresado



def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
	"""
	Decorator for views that checks that the user passes the given test,
	redirecting to the log-in page if necessary. The test should be a callable
	that takes the user object and returns True if the user passes.
	"""

	def decorator(view_func):
		@wraps(view_func)
		def _wrapped_view(request, *args, **kwargs):
			if test_func(request.user):
				return view_func(request, *args, **kwargs)
			path = request.build_absolute_uri()
			resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
			# If the login url is the same scheme and net location then just
			# use the path as the "next" url.
			login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
			current_scheme, current_netloc = urlparse(path)[:2]
			if ((not login_scheme or login_scheme == current_scheme) and
					(not login_netloc or login_netloc == current_netloc)):
				path = request.get_full_path()
			from django.contrib.auth.views import redirect_to_login
			return redirect_to_login(
				path, resolved_login_url, redirect_field_name)
		return _wrapped_view
	return decorator
	
def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
	"""
	Decorator for views that checks that the user is logged in, redirecting
	to the log-in page if necessary.
	"""
	actual_decorator = user_passes_test(
		lambda u: u.is_authenticated,
		login_url=login_url,
		redirect_field_name=redirect_field_name
	)
	if function:
		return actual_decorator(function)
	return actual_decorator

def primerLogin(index_url=None, raise_exception=False, isNotYet=True):
	def check(user):
		try:
			usuario=User.objects.get(username=user)
			usuario=UsuariosAdminEgresado.objects.get(user_id=usuario.id)
		except:
			usuario=None
			if raise_exception:
				raise PermissionDenied
			return False
		

		if(not usuario.pais=="" and isNotYet):
			return True
		elif(usuario.pais=="" and not isNotYet):
			return True
		if raise_exception:
			raise PermissionDenied
		return False
	#print(index_url)
	return user_passes_test(check, login_url=index_url)
	
def redirectEgresado(index_url=None, raise_exception=False):
	def determinarTipoUser(username):
		try:
			user=User.objects.get(username=username)
			user=UsuariosAdminEgresado.objects.get(user_id=user.id)
		except:
			index_url="usuario:login"
		try:
			userAdmin=UsuarioAdministrador.objects.get(userAdminEgre_id=user.DNI)
		except:
			userAdmin=None
		
		try:
			userEgre=UsuarioEgresado.objects.get(userAdminEgre_id=user.DNI)
		except:
			userEgre=None
		
		if(userAdmin is not None and userEgre is not None):
			return True
		elif(userAdmin is not None):
			if raise_exception:
				raise PermissionDenied
			return False
			
		elif(userEgre is not None):
			return True
		elif(userAdmin is None and userEgre is None):
			print("ERROR - No se ha logrado determinar el tipo de usuario")
			if raise_exception:
				raise PermissionDenied
			return False
	return user_passes_test(determinarTipoUser, login_url=index_url)