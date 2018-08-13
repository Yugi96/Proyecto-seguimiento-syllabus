from django.urls import path, re_path
from django.contrib.auth.decorators import permission_required
from apps.universidad.views import homeEstudiante, PerfilViewEstudiante, change_password_estudiante, PerfilUpdateEstudianteView
from apps.seguimiento.views import SeguimientoListView, SeguimientoUpdateView, SeguimientoDeleteView
from apps.usuario.views import ListaMensajesEstudianteView

app_name = 'estudiante'

urlpatterns = [
    re_path('^$', homeEstudiante, name='homeEstudiante'),

    re_path('^perfil/$', permission_required('universidad.Estudiante')(PerfilViewEstudiante.as_view()), name='perfil'),
    re_path('^perfil/cambiar-password/$',  permission_required('universidad.Estudiante')(change_password_estudiante), name='cambiar_password'),
    re_path('^perfil/editar/(?P<pk>\d+)/$', permission_required('universidad.Estudiante')(PerfilUpdateEstudianteView.as_view()), name='perfil_editar'),



    re_path('^seguimiento/$', permission_required('universidad.Estudiante')(SeguimientoListView.as_view()), name='seguimientos'),
    re_path('^seguimiento/editar/(?P<pk>\d+)/$', permission_required('universidad.Estudiante')(SeguimientoUpdateView.as_view()), name='seguimientos_editar'),
    re_path('^seguimiento/eliminar/(?P<pk>\d+)/$', permission_required('universidad.Estudiante')(SeguimientoDeleteView.as_view()), name='seguimientos_eliminar'),

    re_path('^mensajes/$', permission_required('universidad.Estudiante')(ListaMensajesEstudianteView.as_view()), name='mensajes'),
    
]