from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Seguimiento

# Create your views here.
class SeguimientoList(ListView):
    model = Seguimiento
    template_name = 'estudiante/seguimiento/index.seguimiento.template.html'