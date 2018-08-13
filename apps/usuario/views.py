from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail

from .models import Mensaje
from .forms import MensajeriaForm

from apps.universidad.models import Curso, Alumno


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

class ListaMensajesView(FormMessageMixin, CreateView):
    form_class = MensajeriaForm
    success_url = reverse_lazy('coordinador:mensajes')
    template_name = 'coordinador/mensajes.coordinador.template.html'
    form_valid_message = 'MENSAJE ENVIADO CON EXITO'
    form_invalid_message = "ERROR: NO SE PUEDO ENVIAR EL MENSAJE"

    def get_context_data(self, **kwargs):
        context = super(ListaMensajesView, self).get_context_data(**kwargs)
        context['mensajes_recibidos'] = Mensaje.objects.filter(men_estado=True, usuario_destinatario=self.request.user).order_by('men_fecha')
        # kwargs['object_list'] = Mensaje.objects.filter(men_estado=True, usuario_destinatario=self.request.user).order_by('men_fecha')
        # kwargs['object_list'] = Mensaje.objects.filter(men_estado=True).order_by('men_fecha')
        return context

    def get_form(self, form_class=None):
        form = super(ListaMensajesView,self).get_form(form_class) #instantiate using parent
        form.request = self.request
        fullNameRemitente = User.objects.filter(username=self.request.user.username)
        noMostrar = [self.request.user.username, 'admin']
        cursos = Curso.objects.all()
        alumnos = []
        coordinador = User.objects.get(user_permissions=29)
        print(coordinador)
        for curso in cursos:
            alumnos.append(curso.alumno.usuario)
        alumnos.append(coordinador)
        fullNameDestiatario = User.objects.filter(username__in=alumnos).exclude(username__in=noMostrar)
        form.fields['usuario_remitente'].choices = [(user.pk, user.get_full_name()) for user in fullNameRemitente]
        form.fields['usuario_destinatario'].choices = [(user.pk, user.get_full_name()) for user in fullNameDestiatario]
        return form

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        print(request.POST['usuario_remitente'])
        print(request.POST['usuario_destinatario'])
        if form.is_valid():
            destinatarios = []
            for destinatario in form.cleaned_data['usuario_destinatario']:
                destinatarios.append(User.objects.get(username=destinatario).email)
            remitente = User.objects.get(username=form.cleaned_data['usuario_remitente'])
            send_mail(
                'Remitente: {} {} - Asunto: {}'.format(remitente.first_name, remitente.last_name, form.cleaned_data['men_asunto']),
                form.cleaned_data['men_mensaje'],
                None,
                destinatarios,
            )
            form.save()
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

class ListaMensajesEstudianteView(FormMessageMixin, CreateView):
    form_class = MensajeriaForm
    success_url = reverse_lazy('estudiante:mensajes')
    template_name = 'estudiante/mensajes.estudiante.template.html'
    form_valid_message = 'MENSAJE ENVIADO CON EXITO'
    form_invalid_message = "ERROR: NO SE PUEDO ENVIAR EL MENSAJE"

    def get_context_data(self, **kwargs):
        context = super(ListaMensajesEstudianteView, self).get_context_data(**kwargs)
        context['mensajes_recibidos'] = Mensaje.objects.filter(men_estado=True, usuario_destinatario=self.request.user).order_by('men_fecha')
        # kwargs['object_list'] = Mensaje.objects.filter(men_estado=True, usuario_destinatario=self.request.user).order_by('men_fecha')
        # kwargs['object_list'] = Mensaje.objects.filter(men_estado=True).order_by('men_fecha')
        return context

    def get_form(self, form_class=None):
        form = super(ListaMensajesEstudianteView,self).get_form(form_class) #instantiate using parent
        form.request = self.request
        fullNameRemitente = User.objects.filter(username=self.request.user.username)
        noMostrar = [self.request.user.username, 'admin']
        cursos = Curso.objects.all()
        alumnos = []
        coordinador = User.objects.get(user_permissions=29)
        print(coordinador)
        for curso in cursos:
            alumnos.append(curso.alumno.usuario)
        alumnos.append(coordinador)
        fullNameDestiatario = User.objects.filter(username__in=alumnos).exclude(username__in=noMostrar)
        form.fields['usuario_remitente'].choices = [(user.pk, user.get_full_name()) for user in fullNameRemitente]
        form.fields['usuario_destinatario'].choices = [(user.pk, user.get_full_name()) for user in fullNameDestiatario]
        return form

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        print(request.POST['usuario_remitente'])
        print(request.POST['usuario_destinatario'])
        if form.is_valid():
            destinatarios = []
            for destinatario in form.cleaned_data['usuario_destinatario']:
                destinatarios.append(User.objects.get(username=destinatario).email)
            remitente = User.objects.get(username=form.cleaned_data['usuario_remitente'])
            # send_mail(
            #     'Remitente: {} {} - Asunto: {}'.format(remitente.first_name, remitente.last_name, form.cleaned_data['men_asunto']),
            #     form.cleaned_data['men_mensaje'],
            #     None,
            #     destinatarios,
            # )
            form.save()
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)