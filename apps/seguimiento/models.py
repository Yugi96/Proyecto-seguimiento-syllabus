from django.db import models
from apps.universidad.models import Asignatura, Docente, Periodo, Semestre

# Create your models here.
class Horario(models.Model):
    # LUNES = 'LUN'
    # MARTES = 'MAR'
    # MIERCOLES = 'MIR'
    # JUEVES = 'JUE'
    # VIERNES = 'VIE'
    # DIAS = (
    #     (LUNES, 'LUNES'),
    #     (MARTES, 'MARTES'),
    #     (MIERCOLES, 'MIERCOLES'),
    #     (JUEVES, 'JUEVES'),
    #     (VIERNES, 'VIERNES'),
    # )
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    hor_paralelo = models.CharField(max_length=5)
    hor_dia = models.CharField(max_length=15)
    hor_horas = models.PositiveIntegerField()
    hor_estado = models.BooleanField(default=True)

class Seguimiento(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    seg_paralelo = models.CharField(max_length=5)
    seg_porcentaje_real = models.PositiveIntegerField()
    seg_porcentaje_ideal = models.PositiveIntegerField()
    seg_observaciones = models.CharField(max_length=100, blank=True, default="")
    seg_semana = models.CharField(max_length=20)
    seg_mes = models.CharField(max_length=20)
    seg_fecha = models.DateField()
    seg_estado = models.BooleanField(default=True)

    class Meta:
        unique_together = ("seg_fecha", "asignatura",)
