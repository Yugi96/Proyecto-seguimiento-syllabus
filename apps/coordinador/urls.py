from django.urls import path, re_path
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from apps.universidad.views import homeCoordinador, UploadFileView, UpdateDocente, UploadFileViewAsignatura

app_name = 'coordinador'

urlpatterns = [
    re_path('^$', homeCoordinador, name='homeCoordinador'),
    re_path('^docentes/$', permission_required('universidad.Coordinador')(UploadFileView.as_view()), name='docentes'),
    re_path('^docentes/editar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(UpdateDocente.as_view()), name='docente_editar'),
    re_path('^asignaturas/$', permission_required('universidad.Coordinador')(UploadFileViewAsignatura.as_view()), name='asignaturas'),
]