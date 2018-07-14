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
            'doc_correo',
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
                'minlength' : '10', 
                'onkeypress' : 'return soloNumeros(event);',
                'autocomplete' : 'off',
                'required' : 'true',
                }),
            'doc_nombres' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'doc_nombres',
                'onkeypress' : 'return soloLetras(event);',
                'onkeyup' : 'convertirMayuscula(this);'
                }),
            'doc_apellidos' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'doc_apellidos',
                'onkeypress' : 'return soloLetras(event);',
                'onkeyup' : 'convertirMayuscula(this);'
                }),
            'doc_telefono' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'doc_telefono',
                'onkeypress' : 'return soloNumeros(event);'
                }),
            'doc_correo' : forms.EmailInput(attrs={'class' : 'input-campo', 'id' : 'doc_correo'}),
        }

class DocenteUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Docente

        fields = [
            'doc_nombres',
            'doc_apellidos',
            'doc_telefono',
            'doc_correo',
            'doc_estado',
        ]

        labels = {
            'doc_nombres' : 'NOMBRES',
            'doc_apellidos' : 'APELLIDOS',
            'doc_telefono' : 'TELÉFONO',
            'doc_correo' : 'CORREO',
            'doc_estado' : 'ESTADO'
        }

        widgets = {
            'doc_nombres' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'doc_nombres',
                'onkeypress' : 'return soloLetras(event);',
                'onkeyup' : 'convertirMayuscula(this);'
                }),
            'doc_apellidos' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'doc_apellidos',
                'onkeypress' : 'return soloLetras(event);',
                'onkeyup' : 'convertirMayuscula(this);'
                }),
            'doc_telefono' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'doc_telefono',
                'onkeypress' : 'return soloNumeros(event);'
                }),
            'doc_correo' : forms.EmailInput(attrs={'class' : 'input-campo', 'id' : 'doc_correo'}),
            'doc_estado' : forms.CheckboxInput(attrs={
                'data-toggle' : 'popover',
                'title' : 'DAR DE BAJA',
                'data-trigger' : 'focus',
                'data-content' : 'AL DAR DE BAJA A UN DOCENTE, ESTE NO SE MOSTRARÁ EN LA LISTA PRINCIPAL. PUEDE ACCEDER A LOS DOCENTES INACTIVOS EN LA OPCIÓN HISTORIA DEL MENÚ LATERAL',
                })
        }


        