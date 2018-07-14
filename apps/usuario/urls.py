from django.conf.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from apps.usuario.views import UserList, UserDetail

app_name = 'usuario'

urlpatterns = [
    re_path('^user/$', UserList.as_view(), name='api'),
    re_path('^user/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='api'),
]

urlpatterns = format_suffix_patterns(urlpatterns)