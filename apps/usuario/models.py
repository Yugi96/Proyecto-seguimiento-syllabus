from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Mensaje(models.Model):
    usuario_remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remitente')
    usuario_destinatario = models.ManyToManyField(User, related_name='destinatario')
    men_asunto = models.CharField(max_length=50, blank=True, null=True)
    men_mensaje = models.CharField(max_length=200)
    men_fecha = models.DateTimeField(auto_now_add=True)
    men_leido = models.BooleanField(default=False)
    men_estado = models.BooleanField(default=True)

class Notificaciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    not_notificacion = models.CharField(max_length=100)
    not_fecha = models.DateTimeField(auto_now_add=True)
    not_leido = models.BooleanField(default=False)
    not_estado = models.BooleanField(default=True)