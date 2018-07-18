from django import forms

from apps.universidad.models import Docente, Asignatura, Semestre, Periodo, Asignatura_Docente

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
                'class' : 'form-control datepicker input-campo', 
                'id' : 'per_inicio',
            }),
            'per_fin' : forms.DateInput(attrs={
                'class' : 'form-control datepicker input-campo',
                'id' : 'per_fin',
            }),
        }

class AsignaturaDocenteForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (AsignaturaDocenteForm,self ).__init__(*args,**kwargs)
        docentesList = Asignatura_Docente.objects.filter(asi_doc_estado=True, asi_doc_eliminado=False)
        noMostrarDocentes = []
        for docente in docentesList:
            noMostrarDocentes.append(docente.docente_id)
        self.fields['docente'].queryset = Docente.objects.filter(doc_estado=True).exclude(doc_cedula__in=noMostrarDocentes)
        self.fields['asignatura'].queryset = Asignatura.objects.filter(asi_estado=True)
        self.fields['periodo'].queryset = Periodo.objects.filter(per_estado=True)

    class Meta:
        model = Asignatura_Docente

        fields = [
            'docente',
            'asignatura',
            'periodo',
        ]

        labels = {
            'docente' : 'DOCENTE',
            'asignatura' : 'ASIGNATURAS',
            'periodo' : 'PERIODO',
        }

        widgets = {
            'docente' : forms.Select(attrs={
                'class' : 'custom-select', 
                'id' : 'per_nombre', 
                'required' : 'true',
                'onkeyup' : 'convertirMayuscula(this);'
            }),
            'asignatura' : forms.CheckboxSelectMultiple(attrs={
                'class' : 'form-control campo-check-mul h-100 ', 
                'id' : 'per_inicio',
            }),
            'periodo' : forms.Select(attrs={
                'class' : 'form-control custom-select',
                'id' : 'per_fin',
            }),
        }

class AsignaturaDocenteUpdateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (AsignaturaDocenteUpdateForm,self ).__init__(*args,**kwargs)
        self.fields['asignatura'].queryset = Asignatura.objects.filter(asi_estado=True)

    class Meta:
        model = Asignatura_Docente

        fields = [
            'asignatura',
            'asi_doc_eliminado'
        ]

        labels = {
            'asignatura' : 'ASIGNATURAS',
            'asi_doc_eliminado' : 'QUITAR'
        }

        widgets = {
            'asignatura' : forms.CheckboxSelectMultiple(attrs={
                'class' : 'form-control campo-check-mul h-100 ', 
                'id' : 'per_inicio',
            }),
            'asi_doc_eliminado' : forms.CheckboxInput(attrs={
                'data-toggle' : 'popover',
                'title' : 'DAR DE BAJA',
                'class' : 'campo-check',
                'data-trigger' : 'focus',
                'data-content' : 'AL DAR DE BAJA A UN DOCENTE, ESTE NO SE MOSTRARÁ EN LA LISTA PRINCIPAL. PUEDE ACCEDER A LOS DOCENTES INACTIVOS EN LA OPCIÓN HISTORIA DEL MENÚ LATERAL',
            })
        }