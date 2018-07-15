from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Unidad_Academica(models.Model):
    uni_codigo = models.CharField(max_length=6, primary_key=True)
    uni_nombre = models.CharField(max_length=100)
    uni_abreviatura = models.CharField(max_length=10)

class Carrera(models.Model):
    car_codigo = models.CharField(max_length=6, primary_key=True)
    uni_codigo = models.ForeignKey(Unidad_Academica, on_delete=models.CASCADE)
    car_nombre = models.CharField(max_length=50)
    car_estado = models.BooleanField(default=True)

    def getCarNombre(self):
        return self.car_nombre

    def __str__(self):
        return self.car_nombre

class Periodo(models.Model):
    per_codigo = models.CharField(max_length=6, primary_key=True)
    per_nombre = models.CharField(max_length=10)
    per_inicio = models.DateField()
    per_fin = models.DateField()
    per_estado = models.BooleanField(default=True)

    def __str__(self):
        return self.per_nombre

class Semestre(models.Model):
    sem_codigo = models.CharField(max_length=6, primary_key=True)
    sem_nombre = models.CharField(max_length=30)
    sem_estado = models.BooleanField(default=True)

    def __str__(self):
        return self.sem_nombre

class Alumno(models.Model):
    alu_cedula = models.CharField(max_length=10, primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    alu_observacion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:

        permissions = (
            ('Estudiante', 'Es Estudiante'),
            ('Coordinador', 'Es Coordinador'),
        )

class Curso(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    cur_paralelo = models.CharField(max_length=5)
    cur_estado = models.BooleanField(default=True)

class Asignatura(models.Model):
    asi_codigo = models.CharField(max_length=20, primary_key=True)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, default="")
    asi_nombre = models.CharField(max_length=50, unique=True)
    asi_num_creditos = models.PositiveIntegerField()
    asi_estado = models.BooleanField(default=True)

    def __str__(self):
        return "{} | {} | {}".format(self.asi_nombre, self.semestre, self.semestre.carrera)

class Docente(models.Model):
    doc_cedula = models.CharField(max_length=10, primary_key=True)
    doc_nombres = models.CharField(max_length=50)
    doc_apellidos = models.CharField(max_length=50)
    doc_telefono = models.CharField(max_length=10)
    doc_correo = models.EmailField(max_length=50)
    doc_estado = models.BooleanField(default=True)
    asignaturas = models.ManyToManyField(Asignatura, through='Asignatura_Docente', through_fields=('docente', 'asignatura'),)

    def __str__(self):
        return "{} {}".format(self.doc_nombres, self.doc_apellidos)

class Asignatura_Docente(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    asi_doc_estado = models.BooleanField(default=True)

    def __str__(self):
        return "{} | {} ".format(self.docente, self.asignatura)




