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

from .models import Docente, Asignatura, Semestre, Periodo, Curso, Asignatura_Docente, Alumno, Curso

# Import Docentes
from .forms import DocenteForm, DocenteUpdateForm 
# Import Asignaturas
from .forms import AsignaturaForm, AsignaturaUpdateForm
# Import Estudiante Curso
from .forms import AlumnoForm, CursoForm, UserForm, UserUpdateForm, AlumnoUpdateForm
# Import Periodo
from .forms import PeriodoForm
# Import Asignatura Docente
from .forms import AsignaturaDocenteForm, AsignaturaDocenteUpdateForm

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

class FormMessageMixin(object):
    @property
    def form_valid_message(self):
        return NotImplemented

    # form_invalid_message = 'ERROR: EL NÚMERO DE CÉDULA YA EXISTE'

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
    form_valid_message = 'DOCENTE AGREGADO CON EXITO'
    form_invalid_message = "ERROR: EL NÚMERO DE CÉDULA YA EXISTE"

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Docente.objects.filter(doc_estado=True).order_by('doc_apellidos')
        return super(UploadFileView, self).get_context_data(**kwargs)

class UpdateDocente(FormMessageMixin, UpdateView):
    model = Docente
    form_class = DocenteUpdateForm
    success_url = reverse_lazy('coordinador:docentes')
    template_name = 'coordinador/docente/actualizar.docente.template.html'
    form_valid_message = 'DOCENTE ACTUALIZADO CON EXITO'
    form_invalid_message = "ERROR: ERROR AL ACTUALIZAR EL DOCENTE"

class UploadFileViewAsignatura(FormMessageMixin, CreateView):
    form_class = AsignaturaForm
    success_url = reverse_lazy('coordinador:asignaturas')
    template_name = 'coordinador/asignatura/index.asignatura.is.template.html'
    form_valid_message = 'ASIGNATURA AGREGADA CON EXITO'
    form_invalid_message = "ERROR: LA ASIGNATURA YA EXISTE"

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Asignatura.objects.filter(asi_estado=True).order_by('asi_nombre')
        return super(UploadFileViewAsignatura, self).get_context_data(**kwargs)

class UpdateAsignatura(FormMessageMixin, UpdateView):
    model = Asignatura
    form_class = AsignaturaUpdateForm
    success_url = reverse_lazy('coordinador:asignaturas')
    template_name = 'coordinador/asignatura/actualizar.asignatura.template.html'
    form_valid_message = 'ASIGNATURA ACTUALIZADO CON EXITO'
    form_invalid_message = "ERROR: ERROR AL ACTUALIZAR ASIGNATURA"

class PeriodoView(FormMessageMixin, CreateView):
    form_class = PeriodoForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/index.periodo.template.html'
    form_valid_message = 'PERIODO AGREGADO CON EXITO'
    form_invalid_message = "ERROR: NO SE PUDO INGRESAR EL PERIODO"
    
    def get_context_data(self, **kwargs):
        context = super(PeriodoView, self).get_context_data(**kwargs)
        context['periodos_list'] = Periodo.objects.filter(per_estado=True)
        if len(context['periodos_list']) != 0:
            context['cursos_list'] = Curso.objects.filter(cur_estado=True, periodo_id = context['periodos_list'][0].id ).order_by('alumno')
        if len(context['periodos_list']) != 0:
            context['docentes_asingaturas_list'] = Asignatura_Docente.objects.filter(asi_doc_estado=True, asi_doc_eliminado=False, periodo_id = context['periodos_list'][0].id ).order_by('docente')
        return context

class AsignaturaDocenteView(FormMessageMixin, CreateView):
    form_class = AsignaturaDocenteForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/agregar_docente.periodo.template.html'
    form_valid_message = 'ASIGNATURAS AGREGADAS CON EXITO'
    form_invalid_message = "ERROR: NO SE PUDO AGREGAR EL REGISTRO"

class AsignaturaDocenteUpdateView(FormMessageMixin, UpdateView):
    model = Asignatura_Docente
    form_class = AsignaturaDocenteUpdateForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'coordinador/periodo/editar_docente.periodo.template.html'
    form_valid_message = 'ASIGNATURAS ACTUALIZADA CON EXITO'
    form_invalid_message = "ERROR: NO SE PUDO ACTUALIZAR EL REGISTRO"


class EstudianteView(FormMessageMixin, CreateView):
    model = Alumno
    form_class = AlumnoForm
    second_form_class = UserForm
    template_name = 'coordinador/estudiante/index.estudiante.template.html'
    form_valid_message = 'ESTUDIANTE INGRESADO CON EXITO'
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
            user.password = make_password('8v0Semestre2019')
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
    form_valid_message = 'ESTUDIANTE ACTUALIZADO CON EXITO'
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
            form.save()
            form2.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
