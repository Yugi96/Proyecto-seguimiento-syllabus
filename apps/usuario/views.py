from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Mensaje
from .forms import MensajeriaForm


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
        # kwargs['object_list'] = Mensaje.objects.filter(men_estado=True, usuario_destinatario=self.request.user).order_by('men_fecha')
        kwargs['object_list'] = Mensaje.objects.filter(men_estado=True).order_by('men_fecha')
        return super(ListaMensajesView, self).get_context_data(**kwargs)

    def get_form(self, form_class=None):
        form = super(ListaMensajesView,self).get_form(form_class) #instantiate using parent
        form.request = self.request
        form.fields['usuario_remitente'].queryset = User.objects.filter(username=self.request.user.username)
        fullNameRemitente = User.objects.filter(username=self.request.user.username)
        noMostrar = [self.request.user.username, 'admin']
        form.fields['usuario_destinatario'].queryset = User.objects.exclude(username__in=noMostrar)
        fullNameDestiatario = User.objects.exclude(username__in=noMostrar)
        form.fields['usuario_remitente'].choices = [(user.pk, user.get_full_name()) for user in fullNameRemitente]
        form.fields['usuario_destinatario'].choices = [(user.pk, user.get_full_name()) for user in fullNameDestiatario]
        return form