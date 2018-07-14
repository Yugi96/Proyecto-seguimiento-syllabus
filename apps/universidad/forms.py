from django import forms

from apps.universidad.models import Docente

class DocenteForm(forms.ModelForm):
    
    class Meta:
        model = Docente

        fields = [
            'doc_cedula',
            'doc_nombres',
            'doc_apellidos',
            'doc_telefono',
            'doc_correo'
        ]

        labels = {
            'doc_cedula' : 'CÉDULA',
            'doc_nombres' : 'NOMBRES',
            'doc_apellidos' : 'APELLIDOS',
            'doc_telefono' : 'TELÉFONO',
            'doc_correo' : 'CORREO',
        }

        widgets = {
            'doc_cedula' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'doc_cedula', 
                'maxlength' : '10', 
                'onkeypress' : 'return soloNumeros(event);',
                'autocomplete' : 'off',
                'required' : 'true',
                }),
            'doc_nombres' : forms.TextInput(attrs={'class' : 'input-campo', 'id' : 'doc_nombres'}),
            'doc_apellidos' : forms.TextInput(attrs={'class' : 'input-campo', 'id' : 'doc_apellidos'}),
            'doc_telefono' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'doc_telefono',
                'onkeypress' : 'return soloNumeros(event);'
                }),
            'doc_correo' : forms.EmailInput(attrs={'class' : 'input-campo', 'id' : 'doc_correo'}),
        }



        