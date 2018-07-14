from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse

from .models import Docente
from .forms import DocenteForm
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
        return None

    form_invalid_message = 'ERROR: EL NÚMERO DE CÉDULA YA EXISTE'

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

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = Docente.objects.order_by('doc_apellidos')
        return super(UploadFileView, self).get_context_data(**kwargs)

    # def form_invalid(self, form):
    #     return HttpResponseRedirect(self.get_success_url())


