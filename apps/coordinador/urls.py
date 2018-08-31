from django.urls import path, re_path
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from apps.universidad.views import homeCoordinador, UploadFileView, UpdateDocente, \
                                    UploadFileViewAsignatura, UpdateAsignatura, PeriodoView, \
                                    AsignaturaDocenteView, AsignaturaDocenteUpdateView, EstudianteView, \
                                    EstudianteUpdateView, CursoView, CursoUpdateView, PeriodoUpdateView, TerminarPeriodoView, \
                                    CursoRemplazarView, historialMenu, HistorialEstudianteView, HistorialEstudianteUpdateView, \
                                    HistorialDocenteView, HistorialDocenteUpdateView, HistorialAsignaturaView, HistorialAsignaturaUpdateView, \
                                    SeguimientoListView, PerfilView, change_password, \
                                    PerfilUpdateView, IndexView, CarreraUpdateView, HistorialPeriodosView, HistorialPeriodoDetalleView, \
                                    HistorialAsignaturaDocenteView

from apps.seguimiento.views import CursosHorariosListView, HorarioCreateView, HorarioDeleteView, ReportesViewCoordinador, \
                                    MyPDFViewCoordinadorEstudiante, CursosHistorialHorariosListView, HistorialReportesViewCoordinador, \
                                    HistorialMyPDFViewCoordinadorEstudiante, HistorialSeguimientoListView, MyPDFViewMensual, ReportesMensualesView

from apps.usuario.views import ListaMensajesView

app_name = 'coordinador'

urlpatterns = [
    re_path('^$', permission_required('universidad.Coordinador')(IndexView.as_view()), name='homeCoordinador'),
    re_path('^carrera/editar/(?P<pk>.+?)/', permission_required('universidad.Coordinador')(CarreraUpdateView.as_view()), name='carrera_editar'),    
    
    re_path('^perfil/$', permission_required('universidad.Coordinador')(PerfilView.as_view()), name='perfil'),
    re_path('^perfil/cambiar-password/$', permission_required('universidad.Coordinador')(change_password) , name='cambiar_password'),
    re_path('^perfil/editar/(?P<pk>\d+)/$', permission_required('universidad.Coordinador')(PerfilUpdateView.as_view()), name='perfil_editar'),

    re_path('^docentes/$', permission_required('universidad.Coordinador')(UploadFileView.as_view()), name='docentes'),
    re_path('^docentes/editar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(UpdateDocente.as_view()), name='docente_editar'),
    
    re_path('^estudiantes/$', permission_required('universidad.Coordinador')(EstudianteView.as_view()), name='estudiantes'),
    re_path('^estudiantes/editar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(EstudianteUpdateView.as_view()), name='estudiante_editar'),
    
    re_path('^asignaturas/$', permission_required('universidad.Coordinador')(UploadFileViewAsignatura.as_view()), name='asignaturas'),
    re_path('^asignaturas/editar/(?P<pk>.+?)/', permission_required('universidad.Coordinador')(UpdateAsignatura.as_view()), name='asignaturas_editar'),
    
    re_path('^mensajes/$', permission_required('universidad.Coordinador')(ListaMensajesView.as_view()), name='mensajes'),
    
    re_path('^periodo/$', permission_required('universidad.Coordinador')(PeriodoView.as_view()), name='periodos'),
    re_path('^periodo/editar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(PeriodoUpdateView.as_view()), name='periodo_editar'),
    re_path('^periodo/terminar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(TerminarPeriodoView.as_view()), name='periodo_terminar'),

    re_path('^periodo/asignaturas-docente$', permission_required('universidad.Coordinador')(AsignaturaDocenteView.as_view()), name='periodos_docentes_agregar'),
    re_path('^periodo/asignaturas-docente/editar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(AsignaturaDocenteUpdateView.as_view()), name='periodos_docentes_editar'),
    
    re_path('^periodo/curso$', permission_required('universidad.Coordinador')(CursoView.as_view()), name='periodos_curso_agregar'),
    re_path('^periodo/curso/editar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(CursoUpdateView.as_view()), name='periodos_curso_editar'),
    re_path('^periodo/curso/remplazar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(CursoRemplazarView.as_view()), name='periodos_curso_remplazar'),
    
    re_path('^periodo/curso/horario/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(CursosHorariosListView.as_view()), name='periodos_curso_horario'),
    re_path('^periodo/curso/horario/crear/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(HorarioCreateView.as_view()), name='periodos_curso_horario_crear'),
    re_path('^periodo/curso/horario/eliminar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(HorarioDeleteView.as_view()), name='periodos_curso_horario_eliminar'),
    
    re_path('^periodo/curso/seguimiento/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(SeguimientoListView.as_view()), name='periodos_curso_seguimiento'),
    
    re_path('^historial/$', permission_required('universidad.Coordinador')(historialMenu), name='historial'),
    
    re_path('^historial/estudiantes/$', permission_required('universidad.Coordinador')(HistorialEstudianteView.as_view()), name='historial_estudiante'),
    re_path('^historial/estudiantes/editar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(HistorialEstudianteUpdateView.as_view()), name='historial_estudiante_editar'),
    
    re_path('^historial/docentes/$', permission_required('universidad.Coordinador')(HistorialDocenteView.as_view()), name='historial_docente'),
    re_path('^historial/docentes/editar/(?P<pk>\d+)/', permission_required('universidad.Coordinador')(HistorialDocenteUpdateView.as_view()), name='historial_docente_editar'),
    
    re_path('^historial/asignaturas/$', permission_required('universidad.Coordinador')(HistorialAsignaturaView.as_view()), name='historial_asignatura'),
    re_path('^historial/asignaturas/editar/(?P<pk>.+?)/', permission_required('universidad.Coordinador')(HistorialAsignaturaUpdateView.as_view()), name='historial_asignaturas_editar'),

    re_path('^historial/periodos/$', permission_required('universidad.Coordinador')(HistorialPeriodosView.as_view()), name='historial_periodos'),
    re_path('^historial/periodo/(?P<pk>.+?)/$', permission_required('universidad.Coordinador')(HistorialPeriodoDetalleView.as_view()), name='historial_periodo'),
    re_path('^historial/periodo/curso/horario/(?P<pk>.+?)', permission_required('universidad.Coordinador')(CursosHistorialHorariosListView.as_view()), name='historial_periodo_horario'),
    re_path('^historial/periodo/curso/reportes/(?P<pk>.+?)', permission_required('universidad.Coordinador')(HistorialReportesViewCoordinador.as_view()), name='historial_periodo_reporte'),
    re_path('^historial/periodo/curso/report/(?P<seg_semana>\d+)/(?P<pk>.+?)', permission_required('universidad.Coordinador')(HistorialMyPDFViewCoordinadorEstudiante.as_view()), name='historial_periodo_report'),
    re_path('^historial/periodo/curso/seguimiento/(?P<pk>.+?)', permission_required('universidad.Coordinador')(HistorialSeguimientoListView.as_view()), name='historial_seguimiento'),
    re_path('^historial/periodo/asignaturas-docente/(?P<pk>.+?)', permission_required('universidad.Coordinador')(HistorialAsignaturaDocenteView.as_view()), name='historial_docentes_asignaturas'),


    re_path('^reportes/(?P<pk>.+?)/$', permission_required('universidad.Coordinador')(ReportesViewCoordinador.as_view()), name='reportes'),
    # re_path('^reportes/mensuales-(?P<pk>\d+)', permission_required('universidad.Coordinador')(ReportesMensualesView.as_view()), name='reportes_mensuales'),

    re_path('^reporte/(?P<pk>.+?)/(?P<seg_semana>\d+)/$', permission_required('universidad.Coordinador')(MyPDFViewCoordinadorEstudiante.as_view()), name='report'),
    # re_path('^reporte/mensual/(?P<periodo>\d+)/(?P<semanas>.+?)/$', permission_required('universidad.Coordinador')(MyPDFViewMensual.as_view()), name='report_mensual'),

]