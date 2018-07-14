from django.urls import path, re_path
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from apps.universidad.views import homeEstudiante

app_name = 'estudiante'

urlpatterns = [
    re_path('^$', homeEstudiante, name='homeEstudiante'),
]