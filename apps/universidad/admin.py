from django.contrib import admin
from .models import Carrera, Asignatura, Asignatura_Docente, Docente, Periodo, Semestre, Alumno, Curso

# Register your models here.
admin.site.register(Carrera)
admin.site.register(Asignatura)
admin.site.register(Asignatura_Docente)
admin.site.register(Docente)
admin.site.register(Periodo)
admin.site.register(Semestre)
admin.site.register(Alumno)
admin.site.register(Curso)



