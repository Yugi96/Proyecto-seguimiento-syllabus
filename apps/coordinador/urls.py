from django.urls import path, re_path
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from apps.universidad.views import homeCoordinador, UploadFileView

app_name = 'coordinador'

urlpatterns = [
    re_path('^$', homeCoordinador, name='homeCoordinador'),
    re_path('^docentes/$', permission_required('universidad.Coordinador')(UploadFileView.as_view()), name='docentes'),
]