from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core import serializers
from django.db import IntegrityError

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from datetime import datetime

from .models import Docente, Asignatura, Semestre, Periodo, Curso, Asignatura_Docente, Alumno, Curso, Unidad_Academica, Carrera

# Import Docentes
from .forms import DocenteForm, DocenteUpdateForm 
# Import Unidad academica
from .forms import CarreraForm, CarreraUpdateForm
# Import Asignaturas
from .forms import AsignaturaForm, AsignaturaUpdateForm
# Import Estudiante Curso
from .forms import AlumnoForm, CursoForm, UserForm, UserUpdateForm, UserUpdatePerfilEstudianteForm,UserUpdatePerfilCoordinadorForm, AlumnoUpdateForm, CursoUpdateForm, CursoRemplazarForm
# Import Periodo
from .forms import PeriodoForm, TerminarPeriodoForm
# Import Asignatura Docente
from .forms import AsignaturaDocenteForm, AsignaturaDocenteUpdateForm
# Import Historial Estudiantes
from .forms import HistorialAlumnoUpdateForm, HistorialDocenteUpdateForm, HistorialAsignaturaUpdateForm

from apps.seguimiento.forms import SeguimientoForm

from apps.seguimiento.models import Seguimiento, Horario

@login_required
def home(request):
    user = request.user
    if user.has_perm('universidad.Estudiante'):
        return redirect(reverse_lazy('estudiante:homeEstudiante'))
    elif user.has_perm('universidad.Coordinador'):
        return redirect(reverse_lazy('coordinador:homeCoordinador'))
    else:
        return render(request, template_name='universidad/docente/index.template.html')

@permission_required('universidad.Estudiante')
def homeEstudiante(request):
    return render(request, template_name='estudiante/index.estudiante.template.html')

@permission_required('universidad.Coordinador')
def homeCoordinador(request):
    return render(request, template_name='coordinador/index.coordinador.template.html')

def historialMenu(request):
    return render(request, template_name='coordinador/historial/index.historial.template.html')

class FormMessageMixin(object):
    @property
    def form_valid_message(self):
        return NotImplemented

    def form_valid(self, form):
        messages.success(self.request, self.form_valid_message)
        return super(FormMessageMixin, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.form_invalid_message)
        return super(FormMessageMixin, self).form_invalid(form)

class UploadFileView(FormMessageMixin, CreateView):
    form_class = DocenteForm
    success_url = reverse_lazy('coordinador:docentes')
    template_name = 'coordinador/docente/index.docente.template.html'
    form_valid_message = 'DOCENTE AGREGADO CON ÉXITO'
    form_invalid_message = "ERROR: EL NÚMERO DE CÉDULA YA EXISTE"

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Docente.objects.filter(doc_estado=True).order_by('doc_apellidos')
        return super(UploadFileView, self).get_context_data(**kwargs)

class UpdateDocente(FormMessageMixin, UpdateView):
    model = Docente
    form_class = DocenteUpdateForm
    success_url = reverse_lazy('coordinador:docentes')
    template_name = 'coordinador/docente/actualizar.docente.template.html'
    form_valid_message = 'DOCENTE ACTUALIZADO CON ÉXITO'
    form_invalid_message = "ERROR: ERROR AL ACTUALIZAR EL DOCENTE"

class UploadFileViewAsignatura(FormMessageMixin, CreateView):
    form_class = AsignaturaForm
    success_url = reverse_lazy('coordinador:asignaturas')
    template_name = 'coordinador/asignatura/index.asignatura.is.template.html'
    form_valid_message = 'ASIGNATURA AGREGADA CON ÉXITO'
    form_invalid_message = "ERROR: LA ASIGNATURA YA EXISTE"

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Asignatura.objects.filter(asi_estado=True).order_by('carrera','semestre')
        return super(UploadFileViewAsignatura, self).get_context_data(**kwargs)

class UpdateAsignatura(FormMessageMixin, UpdateView):
    model = Asignatura
    form_class = AsignaturaUpdateForm
    success_url = reverse_lazy('coordinador:asignaturas')
    template_name = 'coordinador/asignatura/actualizar.asignatura.template.html'
    form_valid_message = 'ASIGNATURA ACTUALIZADO CON ÉXITO'
    form_invalid_message = "ERROR: ERROR AL ACTUALIZAR ASIGNATURA"

class PeriodoView(FormMessageMixin, CreateView):
    form_class = PeriodoForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/index.periodo.template.html'
    form_valid_message = 'PERIODO AGREGADO CON ÉXITO'
    
    def get_context_data(self, **kwargs):
        context = super(PeriodoView, self).get_context_data(**kwargs)
        context['periodos_list'] = Periodo.objects.filter(per_estado=True)
        if len(context['periodos_list']) != 0:
            context['cursos_list'] = Curso.objects.filter(cur_estado=True, cur_eliminado=False, periodo_id = context['periodos_list'][0].id ).order_by('alumno')
            context['docentes_asingaturas_list'] = Asignatura_Docente.objects.filter(asi_doc_estado=True, asi_doc_eliminado=False, periodo_id = context['periodos_list'][0].id ).order_by('docente')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        periodoInicio = request.POST["per_inicio"]
        periodoFin = request.POST["per_fin"]
        periodoInicio = datetime.strptime(periodoInicio, '%d/%m/%Y')
        periodoFin = datetime.strptime(periodoFin, '%d/%m/%Y')
        if periodoInicio >= periodoFin:
            form_invalid_message = "ERROR: LA FECHA DE INICIO DEBE SER MENOR A LA DE FIN."
            return self.form_invalid(form, form_invalid_message)
        if form.is_valid():
            form.save()
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, "ERROR: PERIODO EXISTENTE")
    
    def form_invalid(self, form, form_invalid_message):
        messages.error(self.request, form_invalid_message)
        return super(PeriodoView, self).form_invalid(form)

class PeriodoUpdateView(UpdateView):
    model = Periodo
    form_class = PeriodoForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/actualizar.periodo.template.html'
    form_valid_message = 'PERIODO ACTUALIZADO CON ÉXITO'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_periodo = kwargs['pk']
        periodo = self.model.objects.get(id=id_periodo)
        form = self.form_class(request.POST, instance=periodo)
        periodoInicio = request.POST["per_inicio"]
        periodoFin = request.POST["per_fin"]
        periodoInicio = datetime.strptime(periodoInicio, '%d/%m/%Y')
        periodoFin = datetime.strptime(periodoFin, '%d/%m/%Y')
        if periodoInicio >= periodoFin:
            form_invalid_message = "ERROR: LA FECHA DE INICIO DEBE SER MENOR A LA DE FIN."
            return self.form_invalid(form, form_invalid_message)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form, "ERROR: NO SE PUDO INGRESAR EL PERIODO")
    
    def form_invalid(self, form, form_invalid_message):
        messages.error(self.request, form_invalid_message)
        return super(PeriodoUpdateView, self).form_invalid(form)

class TerminarPeriodoView(FormMessageMixin, UpdateView):
    model = Periodo
    form_class = TerminarPeriodoForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/terminar.periodo.template.html'
    form_valid_message = 'PERIODO CULMINADO'
    form_invalid_message = "ERROR: NO SE PUDO CULMINAR EL PERIODO"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_periodo = kwargs['pk']
        periodo = self.model.objects.get(id=id_periodo)
        form = self.form_class(request.POST, instance=periodo)
        if form.is_valid():
            docentes = Asignatura_Docente.objects.filter(periodo_id=id_periodo)
            cursos = Curso.objects.filter(periodo_id=id_periodo)
            for docente in docentes:
                docente.asi_doc_estado = False
                docente.save()
            for curso in cursos:
                curso.alumno.usuario.is_active = False
                curso.alumno.usuario.save()
                curso.cur_estado = False
                curso.save()
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class AsignaturaDocenteView(FormMessageMixin, CreateView):
    form_class = AsignaturaDocenteForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/agregar_docente.periodo.template.html'
    form_valid_message = 'ASIGNATURAS AGREGADAS CON ÉXITO'
    form_invalid_message = "ERROR: NO SE PUDO AGREGAR EL REGISTRO"

class HistorialAsignaturaDocenteView(FormMessageMixin, ListView):
    model = Asignatura_Docente
    template_name = 'coordinador/historial/periodo/agregar_docente.periodo.template.html'

    def get_context_data(self, **kwargs):
        context = super(HistorialAsignaturaDocenteView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        context['docente_asignatura_list'] = Asignatura_Docente.objects.get(id=pk)
        return context

class AsignaturaDocenteUpdateView(FormMessageMixin, UpdateView):
    model = Asignatura_Docente
    form_class = AsignaturaDocenteUpdateForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/editar_docente.periodo.template.html'
    form_valid_message = 'ASIGNATURAS ACTUALIZADA CON ÉXITO'
    form_invalid_message = "ERROR: NO SE PUDO ACTUALIZAR EL REGISTRO"

class CursoView(FormMessageMixin, CreateView):
    form_class = CursoForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/agregar_curso.periodo.template.html'
    form_valid_message = 'ESTUDIANTE AGREGADO CON ÉXITO'
    form_invalid_message = "ERROR: YA EXISTE UN ESTUDIANTE EN EL CURSO"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        cursosList = Curso.objects.filter(cur_estado=True, cur_eliminado=False)
        alumnoCarrera = Alumno.objects.filter(id=request.POST['alumno'])
        user = User.objects.get(id=alumnoCarrera[0].usuario_id)
        cursoNuevo = "{} | {} | {} | {}".format(request.POST['semestre'], request.POST['periodo'], request.POST['cur_paralelo'], alumnoCarrera[0].carrera_id)
        for cursoList in cursosList:
            cursoCadena = "{} | {} | {} | {}".format(cursoList.semestre_id, cursoList.periodo_id, cursoList.cur_paralelo, cursoList.alumno.carrera_id)   
            if cursoCadena == cursoNuevo:
                return self.form_invalid(form, **kwargs)
        if form.is_valid():
            form.save()
            user.is_active = True
            user.save()
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

class CursoUpdateView(FormMessageMixin, UpdateView):
    model = Curso
    form_class = CursoUpdateForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/editar_curso.periodo.template.html'
    form_valid_message = 'ESTUDIANTE ACTUALIZADA CON ÉXITO'
    form_invalid_message = "ERROR: YA EXISTE UN ESTUDIANTE EN EL CURSO"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_curso = kwargs['pk']
        curso = self.model.objects.get(id=id_curso)
        form = self.form_class(request.POST, instance=curso)
        cursosList = Curso.objects.filter(cur_estado=True, cur_eliminado=False).exclude(alumno_id = curso.alumno_id)
        alumnoCarrera = Alumno.objects.filter(id=curso.alumno_id)
        user = User.objects.get(id=alumnoCarrera[0].usuario_id)
        cursoNuevo = "{} | {} | {} | {}".format(request.POST['semestre'], curso.periodo_id, request.POST['cur_paralelo'], alumnoCarrera[0].carrera_id)
        for cursoList in cursosList:
            cursoCadena = "{} | {} | {} | {}".format(cursoList.semestre_id, cursoList.periodo_id, cursoList.cur_paralelo, cursoList.alumno.carrera_id)   
            if cursoCadena == cursoNuevo:
                return self.form_invalid(form)
        esEliminado = request.POST.get("cur_eliminado", False)
        if esEliminado == "on":
            user.is_active = False
            user.save()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class CursoRemplazarView(FormMessageMixin, UpdateView):
    model = Curso
    form_class = CursoRemplazarForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/remplazar_curso.periodo.template.html'
    form_valid_message = 'ESTUDIANTE REMPLAZADO CON ÉXITO'
    form_invalid_message = "ERROR: NO SE PUEDE REMPLAZAR EL ESTUDIANTE EN EL CURSO"

    def get_form(self, form_class=None, *args, **kwargs):
        form = super(CursoRemplazarView,self).get_form(form_class) #instantiate using parent
        id_curso = self.kwargs['pk']
        curso = Curso.objects.get(id=id_curso)
        alumnoCarrera = Alumno.objects.get(id=curso.alumno_id)
        alumnosList = Curso.objects.filter(cur_estado=True, cur_eliminado=False)
        noMostrarAlumnos = []
        for alumno in alumnosList:
            noMostrarAlumnos.append(alumno.alumno_id)
        form.fields['alumno'].queryset = Alumno.objects.filter(carrera_id=alumnoCarrera.carrera, alu_estado=True).exclude(id__in=noMostrarAlumnos)
        return form

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_curso = kwargs['pk']
        curso = self.model.objects.get(id=id_curso)
        form = self.form_class(request.POST, instance=curso)
        cursosList = Curso.objects.filter(cur_estado=True, cur_eliminado=False).exclude(alumno_id = curso.alumno_id)
        alumnoCarrera = Alumno.objects.get(id=curso.alumno_id)
        user = User.objects.get(id=alumnoCarrera.usuario_id)
        
        if form.is_valid():
            alumnoCarrera.alu_observacion = request.POST['alu-observacion']
            alumnoCarrera.alu_estado = False
            alumnoCarrera.save()
            user.is_active = False
            user.save()
            alumnoRemplazado = form.save()
            user = User.objects.get(id=alumnoRemplazado.alumno.usuario_id)
            user.is_active = True
            user.save()
            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class EstudianteView(FormMessageMixin, CreateView):
    model = Alumno
    form_class = AlumnoForm
    second_form_class = UserForm
    template_name = 'coordinador/estudiante/index.estudiante.template.html'
    form_valid_message = 'ESTUDIANTE INGRESADO CON ÉXITO'
    form_invalid_message = "ERROR: NO SE PUDO INGRESAR EL ESTUDIANTE"
    success_url = reverse_lazy('coordinador:estudiantes')

    def get_context_data(self, **kwargs):
        context = super(EstudianteView, self).get_context_data(**kwargs)
        context['estudiantes_list'] = Alumno.objects.filter(alu_estado=True).order_by('usuario__first_name', 'usuario__last_name')
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            permission = Permission.objects.get(codename='Estudiante')
            alumno = form.save(commit=False)
            user = form2.save(commit=False)
            user.password = make_password('8v0Semestre2018')
            user.is_active = False
            user.save()
            user.user_permissions.add(permission)
            alumno.usuario = user
            alumno.save()
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

class EstudianteUpdateView(FormMessageMixin, UpdateView):
    model = Alumno
    second_model = User
    template_name = 'coordinador/estudiante/actualizar.estudiante.template.html'
    form_class = AlumnoUpdateForm
    second_form_class = UserUpdateForm
    form_valid_message = 'ESTUDIANTE ACTUALIZADO CON ÉXITO'
    form_invalid_message = "ERROR: NO SE PUDO ACTUALIZAR EL ESTUDIANTE"
    success_url = reverse_lazy('coordinador:estudiantes')

    def get_context_data(self, **kwargs):
        context = super(EstudianteUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        alumno = self.model.objects.get(id=pk)
        usuario = self.second_model.objects.get(id=alumno.usuario_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=usuario)
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_alumno = kwargs['pk']
        alumno = self.model.objects.get(id=id_alumno)
        usuario = self.second_model.objects.get(id=alumno.usuario_id)
        form = self.form_class(request.POST, instance=alumno)
        form2 = self.second_form_class(request.POST, instance=usuario)
        if form.is_valid() and form2.is_valid():
            estudiante = form.save()
            if estudiante.alu_estado == False:
                usuario.is_active = False
                usuario.save()
                form2.save()
            else:
                form2.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class HistorialEstudianteView(ListView):
    model = Alumno
    template_name = 'coordinador/historial/estudiante/index.estudiante.template.html'

    def get_context_data(self, **kwargs):
        context = super(HistorialEstudianteView, self).get_context_data(**kwargs)
        context['estudiantes_list'] = Alumno.objects.filter(alu_estado=False).order_by('usuario__first_name', 'usuario__last_name')
        return context

class HistorialEstudianteUpdateView(FormMessageMixin, UpdateView):
    model = Alumno
    template_name = 'coordinador/historial/estudiante/actualizar.estudiante.template.html'
    form_class = HistorialAlumnoUpdateForm
    form_valid_message = 'ESTUDIANTE ACTUALIZADO CON ÉXITO'
    form_invalid_message = "ERROR: NO SE PUDO ACTUALIZAR EL ESTUDIANTE"
    success_url = reverse_lazy('coordinador:estudiantes')

class HistorialDocenteView(ListView):
    model = Docente
    template_name = 'coordinador/historial/docente/index.docente.template.html'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Docente.objects.filter(doc_estado=False).order_by('doc_apellidos')
        return super(HistorialDocenteView, self).get_context_data(**kwargs)

class HistorialDocenteUpdateView(FormMessageMixin, UpdateView):
    model = Docente
    template_name = 'coordinador/historial/docente/actualizar.docente.template.html'
    form_class = HistorialDocenteUpdateForm
    form_valid_message = 'DOCENTE ACTUALIZADO CON ÉXITO'
    form_invalid_message = "ERROR: NO SE PUDO ACTUALIZAR EL DOCENTE"
    success_url = reverse_lazy('coordinador:docentes')

class HistorialAsignaturaView(ListView):
    model = Asignatura
    template_name = 'coordinador/historial/asignatura/index.asignatura.template.html'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Asignatura.objects.filter(asi_estado=False).order_by('carrera','semestre')
        return super(HistorialAsignaturaView, self).get_context_data(**kwargs)

class HistorialPeriodosView(ListView):
    model = Periodo
    template_name = 'coordinador/historial/periodo/index.periodos.template.html'

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Periodo.objects.filter(per_estado=False).order_by('per_inicio')
        return super(HistorialPeriodosView, self).get_context_data(**kwargs)

class HistorialPeriodoDetalleView(ListView):
    model = Periodo
    template_name = 'coordinador/historial/periodo/detalle.periodo.template.html'
    
    def get_context_data(self, **kwargs):
        context = super(HistorialPeriodoDetalleView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        context['periodos_list'] = Periodo.objects.filter(id=pk)
        if len(context['periodos_list']) != 0:
            context['cursos_list'] = Curso.objects.filter(cur_eliminado=False, periodo_id = pk ).order_by('alumno')
            context['docentes_asingaturas_list'] = Asignatura_Docente.objects.filter(asi_doc_eliminado=False, periodo_id = pk ).order_by('docente')
        return context


class HistorialAsignaturaUpdateView(FormMessageMixin, UpdateView):
    model = Asignatura
    template_name = 'coordinador/historial/asignatura/actualizar.asignatura.template.html'
    form_class = HistorialAsignaturaUpdateForm
    form_valid_message = 'ASIGNATURA ACTUALIZADO CON ÉXITO'
    form_invalid_message = "ERROR: NO SE PUDO ACTUALIZAR EL DOCENTE"
    success_url = reverse_lazy('coordinador:asignaturas')

class IndexView(FormMessageMixin, CreateView):
    template_name = 'coordinador/index.coordinador.template.html'
    form_class = CarreraForm
    success_url = reverse_lazy('coordinador:homeCoordinador')
    form_valid_message = 'CARRERA AGREGADA CON ÉXITO'
    form_invalid_message = 'ERROR: CARRERA EXISTENTE'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['unidad_list'] = Unidad_Academica.objects.get(uni_codigo="UN0001")
        context['carreras_list'] = Carrera.objects.filter(car_estado=True, uni_codigo_id=context['unidad_list'].uni_codigo)
        return context

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object
            form = self.form_class(request.POST)
            unidad_academica = Unidad_Academica.objects.get(uni_codigo="UN0001")
            if form.is_valid():
                carrera = form.save(commit=False)
                carrera.uni_codigo = unidad_academica
                carrera.save()
                return self.form_valid(form, **kwargs)
            else:
                return self.form_invalid(form, **kwargs)
        except IntegrityError as e:
            return self.form_invalid(form, **kwargs)

class CarreraUpdateView(FormMessageMixin, UpdateView):
    model = Carrera
    form_class = CarreraUpdateForm
    success_url = reverse_lazy('coordinador:homeCoordinador')
    template_name = 'coordinador/editar_carrera.coordinador.template.html'
    form_valid_message = 'CARRERA ACTUALIZADA CON ÉXITO'
    form_invalid_message = "ERROR: ERROR AL ACTUALIZAR LA CARRERA"

class SeguimientoListView(FormMessageMixin, CreateView):
    form_class = SeguimientoForm
    success_url = reverse_lazy('coordinador:periodos_curso_seguimiento')
    template_name = 'coordinador/periodo/seguimiento/index.seguimiento.template.html'
    form_valid_message = 'FECHA REGISTRADA CON ÉXITO'
    form_invalid_message = 'ERROR: NO SE PUEDE AGREGAR EL REGISTRO'
    
    def get_context_data(self, **kwargs):
        context = super(SeguimientoListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        curso = Curso.objects.get(id=pk, cur_eliminado=False)
        context['horario_list'] = Horario.objects.filter(
            hor_estado=True, 
            semestre_id=curso.semestre_id, 
            periodo_id=curso.periodo_id, 
            hor_paralelo=curso.cur_paralelo,
            asignatura__carrera=curso.alumno.carrera_id
        ).distinct('asignatura')
        seguimiento = Seguimiento.objects.filter(
            semestre_id=curso.semestre_id, 
            periodo_id=curso.periodo_id, 
            seg_estado=True, 
            seg_paralelo = curso.cur_paralelo
        ).order_by('seg_semana', 'seg_fecha')
        context['horario_completo'] = Horario.objects.filter(
            hor_estado=True, 
            semestre_id=curso.semestre_id, 
            periodo_id=curso.periodo_id, 
            hor_paralelo=curso.cur_paralelo,
            asignatura__carrera=curso.alumno.carrera_id
        )
        context['curso_list'] = curso
        context['seguimiento_list'] = seguimiento
        return context
    
class PerfilView(ListView):
    model = User
    template_name = 'coordinador/usuario/perfil.coordinador.template.html'

class PerfilViewEstudiante(ListView):
    model = User
    template_name = 'estudiante/usuario/perfil.estudiante.template.html'

class PerfilUpdateView(FormMessageMixin, UpdateView):
    model = User
    template_name = 'coordinador/usuario/actualizar_perfil.coordinador.template.html'
    form_class = UserUpdatePerfilCoordinadorForm
    form_valid_message = 'USUARIO ACTUALIZADO CON ÉXITO'
    form_invalid_message = "ERROR: NO SE PUDO ACTUALIZAR EL USUARIO"
    success_url = reverse_lazy('coordinador:perfil')

class PerfilUpdateEstudianteView(FormMessageMixin, UpdateView):
    model = User
    template_name = 'estudiante/usuario/actualizar_perfil.estudiante.template.html'
    form_class = UserUpdatePerfilEstudianteForm
    form_valid_message = 'USUARIO ACTUALIZADO CON ÉXITO'
    form_invalid_message = "ERROR: NO SE PUDO ACTUALIZAR EL USUARIO"
    success_url = reverse_lazy('estudiante:perfil')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'CONTRASEÑA ACTUALIZADA CON ÉXITO.')
            return redirect('coordinador:perfil')
        else:
            return render(request, 'coordinador/usuario/cambiar_password.coordinador.template.html', {
            'form': form
        })
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'coordinador/usuario/cambiar_password.coordinador.template.html', {
            'form': form
        })

def change_password_estudiante(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'CONTRASEÑA ACTUALIZADA CON ÉXITO.')
            return redirect('estudiante:perfil')
        else:
            return render(request, 'estudiante/usuario/cambiar_password.estudiante.template.html', {
                'form': form
            })
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'estudiante/usuario/cambiar_password.estudiante.template.html', {
            'form': form
        })





