from django.contrib import admin
from .models import Mensaje, Notificaciones

# Register your models here.
admin.site.register(Mensaje)
admin.site.register(Notificaciones)
