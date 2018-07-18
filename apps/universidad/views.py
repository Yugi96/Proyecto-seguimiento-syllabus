from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core import serializers

from .models import Docente, Asignatura, Semestre, Periodo, Curso, Asignatura_Docente
from .forms import DocenteForm, DocenteUpdateForm, AsignaturaForm, AsignaturaUpdateForm, PeriodoForm, AsignaturaDocenteForm, AsignaturaDocenteUpdateForm
# Create your views here.

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