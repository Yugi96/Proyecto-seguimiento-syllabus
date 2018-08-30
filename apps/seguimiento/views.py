import datetime

from django.shortcuts import render, redirect

from django.db.models import OuterRef, Subquery
from django.http import HttpResponse
from django.views.generic import View

from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Seguimiento, Horario
from apps.universidad.models import Asignatura_Docente, Curso, Alumno, Asignatura, Semestre, Periodo, Docente
from .forms import SeguimientoForm, HorarioForm, SeguimientoUpdateForm

from wkhtmltopdf.views import PDFTemplateResponse

# Create your views here.

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

class SeguimientoListView(FormMessageMixin, CreateView):
    form_class = SeguimientoForm
    success_url = reverse_lazy('estudiante:seguimientos')
    template_name = 'estudiante/seguimiento/index.seguimiento.template.html'
    form_valid_message = 'FECHA REGISTRADA CON EXITO'
    form_invalid_message = 'ERROR: NO SE PUEDE AGREGAR EL REGISTRO'
    
    def get_context_data(self, **kwargs):
        context = super(SeguimientoListView, self).get_context_data(**kwargs)
        alumno = Alumno.objects.get(usuario_id=self.request.user.id)
        curso = Curso.objects.get(cur_estado=True, alumno_id=alumno.id, cur_eliminado=False)
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
    
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object
            form = self.form_class(request.POST)
            semestre = Semestre.objects.get(sem_nombre=request.POST['seg_semestre'])
            alumno = Alumno.objects.get(usuario_id=self.request.user.id)
            periodo = Periodo.objects.get(per_nombre=request.POST['seg_periodo'])
            asignatura = Asignatura.objects.get(asi_nombre=request.POST['seg_asignatura'])
            nombres_apellidos_docente = request.POST['seg_docente'].split(" ")
            nombres_docente = nombres_apellidos_docente[0] + " " +nombres_apellidos_docente[1]
            apellidos_docente = nombres_apellidos_docente[2] + " " +nombres_apellidos_docente[3]
            docente = Docente.objects.get(doc_nombres=nombres_docente, doc_apellidos=apellidos_docente)
            if form.is_valid():
                seguimiento = form.save(commit=False)
                seguimiento.periodo = periodo
                seguimiento.semestre = semestre
                seguimiento.asignatura = asignatura
                seguimiento.docente = docente
                seguimiento.carrera = alumno.carrera
                seguimiento.seg_paralelo = request.POST['seg_paralelo']
                seguimiento.save()
                return self.form_valid(form, **kwargs)
            else:
                return self.form_invalid(form, "ERROR: FECHA YA EXISTENTE")
        except IntegrityError as e:
            return self.form_invalid(form, "ERROR: FECHA YA EXISTENTE")
    
    def form_invalid(self, form, form_invalid_message):
        messages.error(self.request, form_invalid_message)
        return super(SeguimientoListView, self).form_invalid(form)

class SeguimientoDeleteView(FormMessageMixin, DeleteView):
    model = Seguimiento
    success_url = reverse_lazy('estudiante:seguimientos')
    template_name = 'estudiante/seguimiento/eliminar.seguimiento.template.html'

class SeguimientoUpdateView(FormMessageMixin ,UpdateView):
    model = Seguimiento
    form_class = SeguimientoUpdateForm
    success_url = reverse_lazy('estudiante:seguimientos')
    template_name = 'estudiante/seguimiento/actualizar.seguimiento.template.html'
    form_valid_message = 'REGISTRO ACTUALIZADO CON EXITO'
    form_invalid_message = "ERROR: NO SE PUDO ACTUALIZAR"
    
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object
            id_seguimiento = kwargs['pk']
            seguimiento = self.model.objects.get(id=id_seguimiento)
            form = self.form_class(request.POST, instance=seguimiento)
            if form.is_valid():
                form.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form, "ERROR: NO SE PUDO ACTUALIZAR")
        except IntegrityError as e:
            return self.form_invalid(form, "ERROR: NO SE PUDO ACTUALIZAR")
    
    def form_invalid(self, form, form_invalid_message):
        messages.error(self.request, form_invalid_message)
        return super(SeguimientoUpdateView, self).form_invalid(form)

class CursosHorariosListView(ListView):
    model = Horario
    template_name = 'estudiante/horario/index.horario.template.html'

    def get_context_data(self, **kwargs):
        context = super(CursosHorariosListView, self).get_context_data(**kwargs)
        curso_id = self.kwargs['pk']
        curso = Curso.objects.get(id=curso_id)
        context['horario_list'] = Horario.objects.filter(
            hor_estado=True, 
            semestre_id=curso.semestre_id, 
            periodo_id=curso.periodo_id, 
            hor_paralelo=curso.cur_paralelo,
            asignatura__carrera=curso.alumno.carrera_id
        )
        context['curso_list'] = curso
        return context

class IndexEstudianteView(ListView):
    model = Horario
    template_name = 'estudiante/index.estudiante.template.html'

    def get_context_data(self, **kwargs):
        context = super(IndexEstudianteView, self).get_context_data(**kwargs)
        alumno = Alumno.objects.get(usuario_id=self.request.user.id)
        curso = Curso.objects.get(cur_estado=True, alumno_id=alumno.id, cur_eliminado=False)
        context['horario_list'] = Horario.objects.filter(
            hor_estado=True, 
            semestre_id=curso.semestre_id, 
            periodo_id=curso.periodo_id, 
            hor_paralelo=curso.cur_paralelo,
            asignatura__carrera=curso.alumno.carrera_id
        )
        context['curso_list'] = curso
        return context

class HorarioCreateView(FormMessageMixin, FormView):
    form_class = HorarioForm
    success_url = reverse_lazy('coordinador:periodos')
    template_name = 'estudiante/horario/agregar.horario.template.html'
    form_valid_message = 'HORARIO AGREGADO CON EXITO'
    form_invalid_message = "ERROR: NO SE PUDO AGREGAR EL HORARIO"
    
    def get_context_data(self, **kwargs):
        context = super(HorarioCreateView, self).get_context_data(**kwargs)
        curso_id = self.kwargs['pk']
        curso = Curso.objects.get(id=curso_id)
        asignaturas = Asignatura.objects.filter(semestre_id=curso.semestre_id, carrera_id=curso.alumno.carrera_id, asi_estado=True)
        asignaturas_docentes = Asignatura_Docente.objects.filter(
            periodo_id=curso.periodo_id, 
            asi_doc_estado=True, 
            asi_doc_eliminado=False,
        ).filter(asignatura__semestre = curso.semestre_id, asignatura__carrera=curso.alumno.carrera_id).distinct()
        print(asignaturas_docentes)
        context['curso_list'] = curso
        context['asignatura_docente_list'] = asignaturas_docentes
        context['asignaturas_list'] = asignaturas
        return context

    def form_valid(self, form):
        sentencia = self.request.POST['sentencia']
        rows = sentencia.split(";")
        for row in rows:
            horarioObject = row.split(",")
            if len(horarioObject) != 1:
                asignaturaHorario = Asignatura.objects.get(asi_nombre=horarioObject[0])
                carreraHorario = asignaturaHorario.carrera
                nombresDocenteListHorario = horarioObject[1].split(" ")
                nombres = nombresDocenteListHorario[0] + " "+ nombresDocenteListHorario[1]
                apellidos = nombresDocenteListHorario[2] + " "+ nombresDocenteListHorario[3]
                docenteHorario = Docente.objects.get(doc_nombres=nombres, doc_apellidos=apellidos)
                periodoHorario = Periodo.objects.get(per_nombre=horarioObject[2])
                semestreHorario = Semestre.objects.get(sem_nombre=horarioObject[3])
                paraleloHorario = horarioObject[4]
                diaHorario = horarioObject[5]
                horasHorario = horarioObject[6]
                
                horarioRow = Horario(
                    asignatura=asignaturaHorario,
                    docente=docenteHorario,
                    periodo=periodoHorario,
                    semestre=semestreHorario,
                    carrera=carreraHorario,
                    hor_paralelo=paraleloHorario,
                    hor_dia=diaHorario,
                    hor_horas=horasHorario
                )
                horarioRow.save()  
        
        return super(HorarioCreateView, self).form_valid(form)

class HorarioDeleteView(FormMessageMixin, DeleteView):
    model = Horario
    success_url = reverse_lazy('coordinador:periodos_curso_horario')
    template_name = 'estudiante/horario/eliminar.horario.template.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        curso_id = self.kwargs['pk']
        curso = Curso.objects.get(id=curso_id)
        
        if not queryset:
            raise Http404

        context = {'curso_id':curso}
        return context

    def delete(self, request, *args, **kwargs):
        curso_id = self.kwargs['pk']
        curso = Curso.objects.get(id=curso_id)
        horario = Horario.objects.filter(periodo_id=curso.periodo, hor_paralelo=curso.cur_paralelo, carrera_id=curso.alumno.carrera_id , semestre_id=curso.semestre_id)
        horario.delete()

            
        return HttpResponseRedirect(reverse('coordinador:periodos_curso_horario', kwargs={'pk': curso_id}))

# class GeneratePdf(ListView):
#     def get(self, request, *args, **kwargs):
#         seguimiento = Seguimiento.objects.all().order_by('seg_semana', 'seg_fecha')
#         pdf = render_to_pdf('reportes/reporte.coordinador.html', {'seguimiento_list':seguimiento})
#         return HttpResponse(pdf, content_type='application/pdf')

class ReportesView(ListView):
    model = Seguimiento
    template_name = 'estudiante/reportes/reportes.estudiante.template.html'

    def get_context_data(self, **kwargs):
        context = super(ReportesView, self).get_context_data(**kwargs)
        alumno = Alumno.objects.get(usuario_id=self.request.user.id)
        curso = Curso.objects.get(cur_estado=True, alumno_id=alumno.id, cur_eliminado=False)

        asignaturas = Horario.objects.filter(
            hor_estado=True, 
            semestre_id=curso.semestre_id, 
            periodo_id=curso.periodo_id, 
            hor_paralelo=curso.cur_paralelo,
            asignatura__carrera=curso.alumno.carrera_id
        ).values_list('asignatura__asi_nombre').distinct('asignatura')

        semanas = Seguimiento.objects.filter(
            semestre_id=curso.semestre_id, 
            periodo_id=curso.periodo_id, 
            seg_estado=True, 
            seg_paralelo = curso.cur_paralelo
        ).values_list('seg_semana').order_by('seg_semana').distinct('seg_semana')

        seguimiento = Seguimiento.objects.filter(
            semestre_id=curso.semestre_id, 
            periodo_id=curso.periodo_id, 
            seg_estado=True, 
            seg_paralelo = curso.cur_paralelo
        ).order_by('seg_semana', 'seg_fecha')

        semanasValidas = []
        for semana in semanas:
            porcentajeIdealTotal = 0.0

            for porcentajeIdeal in seguimiento:
                if(semana[0] == porcentajeIdeal.seg_semana):
                    porcentajeIdealTotal = porcentajeIdealTotal + porcentajeIdeal.seg_porcentaje_ideal
            if(porcentajeIdealTotal/len(asignaturas) == 100):
                semanasValidas.append(semana[0])

        context['semanas_list'] = semanasValidas
        # context['seguimiento_list'] = seguimiento
        return context

class MyPDFView(View):
    template='reportes/reporte.estudiante.html'
    
    def get(self, request, seg_semana):
        alumno = Alumno.objects.get(usuario_id=self.request.user.id)
        curso = Curso.objects.get(cur_estado=True, alumno_id=alumno.id, cur_eliminado=False)
        seguimiento = Seguimiento.objects.filter(
            semestre_id=curso.semestre_id, 
            periodo_id=curso.periodo_id, 
            seg_estado=True,
            seg_semana=seg_semana,
            seg_paralelo = curso.cur_paralelo
        ).order_by('seg_fecha', 'asignatura__asi_nombre')
        response = PDFTemplateResponse(request=request,
                                       template=self.template,
                                       filename="reporte-semana"+ seg_semana +".pdf",
                                       context= {
                                        'seguimiento_list':seguimiento,
                                        'curso_list':curso,
                                        'alumno_list':alumno,
                                        },
                                        show_content_in_browser=True,
                                       cmd_options={
                                       "viewport-size" :"100 x 100",
                                       'javascript-delay':3000,
                                       "no-stop-slow-scripts":True,},
                                       
                                       )
        return response


