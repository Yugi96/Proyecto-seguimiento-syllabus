from django import forms

from apps.universidad.models import Docente, Asignatura, Semestre, Periodo

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
                'class' : 'campo-check',
                'data-trigger' : 'focus',
                'data-content' : 'AL DAR DE BAJA A UN DOCENTE, ESTE NO SE MOSTRARÁ EN LA LISTA PRINCIPAL. PUEDE ACCEDER A LOS DOCENTES INACTIVOS EN LA OPCIÓN HISTORIA DEL MENÚ LATERAL',
                })
        }

class AsignaturaForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (AsignaturaForm,self ).__init__(*args,**kwargs)
        self.fields['semestre'].queryset = Semestre.objects.filter(sem_estado=True)

    class Meta:
        model = Asignatura

        fields = [
            'asi_codigo',
            'carrera',
            'semestre',
            'asi_nombre',
            'asi_num_creditos',
        ]

        labels = {
            'asi_codigo' : 'CÓDIGO',
            'carrera' : 'CARRERA',
            'semestre' : 'SEMESTRE',
            'asi_nombre' : 'NOMBRE',
            'asi_num_creditos' : 'NUM. CREDITOS',
        }

        widgets = {
            'asi_codigo' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'asi_codigo', 
                'required' : 'true',
                'onkeyup' : 'convertirMayuscula(this);'
            }),
            'semestre' : forms.Select(attrs={
                'class' : 'custom-select', 
                'id' : 'semestre',
            }),
            'carrera' : forms.Select(attrs={
                'class' : 'custom-select', 
                'id' : 'carrera',
            }),
            'asi_nombre' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'asi_nombres',
                'onkeypress' : 'return soloLetras(event);',
                'onkeyup' : 'convertirMayuscula(this);'
            }),
            'asi_num_creditos' : forms.TextInput(attrs={
                'class' : 'input-campo',
                'onkeypress' : 'return soloNumeros(event);',
                'id' : 'asi_num_creditos',
            }),
        }

class AsignaturaUpdateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (AsignaturaUpdateForm,self ).__init__(*args,**kwargs)
        self.fields['semestre'].queryset = Semestre.objects.filter(sem_estado=True)

    class Meta:
        model = Asignatura

        fields = [
            'carrera',
            'semestre',
            'asi_nombre',
            'asi_num_creditos',
            'asi_estado',
        ]

        labels = {
            'carrera' : 'CARRERA',
            'semestre' : 'SEMESTRE',
            'asi_nombre' : 'NOMBRE',
            'asi_num_creditos' : 'NUM. CREDITOS',
            'asi_estado' : 'ESTADO',
        }

        widgets = {
            'semestre' : forms.Select(attrs={
                'class' : 'custom-select', 
                'id' : 'semestre',
            }),
            'carrera' : forms.Select(attrs={
                'class' : 'custom-select', 
                'id' : 'semestre',
            }),
            'asi_nombre' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'asi_nombres',
                'onkeypress' : 'return soloLetras(event);',
                'onkeyup' : 'convertirMayuscula(this);'
            }),
            'asi_num_creditos' : forms.TextInput(attrs={
                'class' : 'input-campo',
                'onkeypress' : 'return soloNumeros(event);',
                'id' : 'asi_num_creditos',
            }),
            'asi_estado' : forms.CheckboxInput(attrs={
                'data-toggle' : 'popover',
                'title' : 'DAR DE BAJA',
                'class' : 'campo-check',
                'data-trigger' : 'focus',
                'data-content' : 'AL DAR DE BAJA A UNA ASIGNATURA, ESTE NO SE MOSTRARÁ EN LA LISTA PRINCIPAL. PUEDE ACCEDER A LAS ASIGNATURAS INACTIVOS EN LA OPCIÓN HISTORIA DEL MENÚ LATERAL',
            }),
        }


class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo

        fields = [
            'per_nombre',
            'per_inicio',
            'per_fin',
        ]

        labels = {
            'per_nombre' : 'NOMBRE DE LA ETAPA',
            'per_inicio' : 'INICIO DEL PERIODO',
            'per_fin' : 'FIN DEL PERIODO',
        }

        widgets = {
            'per_nombre' : forms.TextInput(attrs={
                'class' : 'input-campo', 
                'id' : 'per_nombre', 
                'required' : 'true',
                'onkeyup' : 'convertirMayuscula(this);'
            }),
            'per_inicio' : forms.DateInput(attrs={
                'class' : 'form-control datepicker', 
                'id' : 'per_inicio',
            }),
            'per_fin' : forms.DateInput(attrs={
                'class' : 'form-control datepicker',
                'id' : 'per_fin',
            }),
        }