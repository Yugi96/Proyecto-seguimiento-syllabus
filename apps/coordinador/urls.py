from django.urls import path, re_path
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from apps.universidad.views import homeCoordinador, UploadFileView, UpdateDocente, \
                                    UploadFileViewAsignatura, UpdateAsignatura, PeriodoView, \
                                    AsignaturaDocenteView, AsignaturaDocenteUpdateView, EstudianteView
from apps.usuario.views import ListaMensajesView

app_name = 'coordinador'

urlpatterns = [
    re_path('^$', homeCoordinador, name='homeCoordinador'),

    re_path('^docentes/$', permission_required('universidad.Coordinador')(UploadFileView.as_view()), name='docentes'),
    re_path('^docentes/editar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(UpdateDocente.as_view()), name='docente_editar'),
    
    re_path('^estudiantes/$', permission_required('universidad.Coordinador')(EstudianteView.as_view()), name='estudiantes'),
    
    re_path('^asignaturas/$', permission_required('universidad.Coordinador')(UploadFileViewAsignatura.as_view()), name='asignaturas'),
    re_path('^asignaturas/editar/(?P<pk>.+?)/', permission_required('universidad.Coordinador')(UpdateAsignatura.as_view()), name='asignaturas_editar'),
    
    re_path('^mensajes/$', permission_required('universidad.Coordinador')(ListaMensajesView.as_view()), name='mensajes'),
    
    re_path('^periodo/$', permission_required('universidad.Coordinador')(PeriodoView.as_view()), name='periodos'),
    re_path('^periodo/asignaturas-docente$', permission_required('universidad.Coordinador')(AsignaturaDocenteView.as_view()), name='periodos_docentes_agregar'),
    re_path('^periodo/asignaturas-docente/editar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(AsignaturaDocenteUpdateView.as_view()), name='periodos_docentes_editar'),
]