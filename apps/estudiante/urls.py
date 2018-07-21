from django.urls import path, re_path
from django.contrib.auth.decorators import login_required, permission_required
from apps.universidad.views import homeEstudiante
from apps.seguimiento.views import SeguimientoList

app_name = 'estudiante'

urlpatterns = [
    re_path('^$', homeEstudiante, name='homeEstudiante'),
    re_path('^seguimiento/$', permission_required('universidad.Estudiante')(SeguimientoList.as_view()), name='seguimiento'),
]