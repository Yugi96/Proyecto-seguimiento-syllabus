"""follomach URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from apps.universidad.views import homeEstudiante, homeCoordinador, home

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^$', home, name='home'),
    re_path('^estudiante/', include('apps.estudiante.urls', namespace='estudiante')),
    re_path('^coordinador/', include('apps.coordinador.urls', namespace='coordinador')),
    # Login
    re_path('^accounts/login', login, { 'template_name' : 'index.html' }, name='login'),
    re_path('^accounts/logout/$', logout_then_login, name='logout'),
    # Reestablecer password
    re_path('^reset/password_reset', password_reset, {
        'template_name':'registrations/password_reset_form.html', 
        'email_template_name':'registrations/password_reset_email.html'
        }, name='password_reset'),
    re_path('^password_reset_done', password_reset_done, {
        'template_name':'registrations/password_reset_done.html'
        }, name="password_reset_done"),
    re_path('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, {
        'template_name':'registrations/password_reset_confirm.html'
        }, name='password_reset_confirm'),
    re_path('^reset/done', password_reset_complete, {
        'template_name':'registrations/password_reset_complete.html'
        }, name="password_reset_complete"),
]
