from django import forms
from django.contrib.auth.models import User

from .models import Mensaje

class MensajeriaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super (MensajeriaForm,self ).__init__(*args,**kwargs)
        # self.fields['usuario_remitente'].queryset = User.objects.filter(username=username)        

    class Meta:
        model = Mensaje

        fields = [
            'usuario_remitente',
            'usuario_destinatario',
            'men_asunto',
            'men_mensaje',
        ]

        labels = {
            'usuario_remitente' : 'REMITENTE',
            'usuario_destinatario' : 'DESTINATARIO',
            'men_asunto' : 'ASUNTO',
            'men_mensaje' : 'MENSAJE',
        }

        widgets = {
            'usuario_remitente' : forms.Select(attrs={
                'class' : 'custom-select select-remitente', 
                'id' : 'usuario_remitente',
            }),
            'usuario_destinatario' : forms.CheckboxSelectMultiple(attrs={
                'class' : 'campo-check-mul', 
                'id' : 'usuario_destinatario',
            }),
            'men_asunto' : forms.TextInput(attrs={
                'class' : 'input-campo asunto-campo', 
                'id' : 'men_asunto',
                }),
            'men_mensaje' : forms.Textarea(attrs={
                'class' : 'input-campo', 
                'id' : 'men_mensaje',
                'placeholder' : 'Escriba su mensaje aqui...'
                }),
        }
