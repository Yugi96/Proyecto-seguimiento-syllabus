from django.urls import path, re_path
from django.contrib.auth.decorators import permission_required
from apps.universidad.views import homeEstudiante
from apps.seguimiento.views import SeguimientoListView, SeguimientoUpdateView, SeguimientoDeleteView
from apps.usuario.views import ListaMensajesEstudianteView

app_name = 'estudiante'

urlpatterns = [
    re_path('^$', homeEstudiante, name='homeEstudiante'),
    re_path('^seguimiento/$', permission_required('universidad.Estudiante')(SeguimientoListView.as_view()), name='seguimientos'),
    re_path('^seguimiento/editar/(?P<pk>\d+)/$', permission_required('universidad.Estudiante')(SeguimientoUpdateView.as_view()), name='seguimientos_editar'),
    re_path('^seguimiento/eliminar/(?P<pk>\d+)/$', permission_required('universidad.Estudiante')(SeguimientoDeleteView.as_view()), name='seguimientos_eliminar'),

    re_path('^mensajes/$', permission_required('universidad.Estudiante')(ListaMensajesEstudianteView.as_view()), name='mensajes'),
    
]