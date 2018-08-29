from django.db import models
from apps.universidad.models import Asignatura, Docente, Periodo, Semestre, Carrera

# Create your models here.
class Horario(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, default="")
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    hor_paralelo = models.CharField(max_length=5)
    hor_dia = models.CharField(max_length=15)
    hor_horas = models.PositiveIntegerField()
    hor_estado = models.BooleanField(default=True)

class Seguimiento(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    seg_paralelo = models.CharField(max_length=5)
    seg_porcentaje_real = models.FloatField()
    seg_porcentaje_ideal = models.FloatField()
    seg_observaciones = models.CharField(max_length=100, blank=True, default="")
    seg_semana = models.CharField(max_length=20)
    seg_fecha = models.DateField()
    seg_estado = models.BooleanField(default=True)

    class Meta:
        unique_together = ("seg_fecha", "asignatura", "seg_semana")
