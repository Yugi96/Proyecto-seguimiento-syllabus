from django import forms

# from apps.universidad.models import Docente, Asignatura, Semestre, Periodo, Asignatura_Docente, Alumno, Curso, Carrera
from .models import Seguimiento

class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = Seguimiento

        fields = [
            'seg_porcentaje_real',
            'seg_porcentaje_ideal',
            'seg_observaciones',
            # 'seg_semana',
            # 'seg_mes',
            'seg_fecha',
        ]

        labels = {
            'seg_porcentaje_real' : 'PORCENTAJE REAL',
            'seg_porcentaje_ideal' : 'PORCENTAJE IDEAL',
            'seg_observaciones' : 'OBSERVACIONES',
            # 'seg_semana' : 'SEMANA',
            # 'seg_mes' : 'MES',
            'seg_fecha' : 'FECHA',
        }

        widgets = {
            'seg_porcentaje_real' : forms.TextInput(attrs={
                'class' : 'input-campo w-50',
                'onkeypress' : 'return soloNumeros(event);',
                'id' : 'asi_num_creditos',
            }),
            'seg_porcentaje_ideal' : forms.TextInput(attrs={
                'class' : 'input-campo w-50',
                'onkeypress' : 'return soloNumeros(event);',
                'id' : 'asi_num_creditos',
            }),
            'seg_observaciones' : forms.Textarea(attrs={
                'class' : 'input-campo observacion-seg',
                'rows' : '2',
                'id' : 'men_mensaje',
                'placeholder' : 'Escriba la observacion aqui...'
            }),
            # 'seg_semana' : forms.TextInput(attrs={
            #     'class' : 'input-campo', 
            #     'id' : 'doc_nombres',
            #     'onkeypress' : 'return soloLetras(event);',
            #     'onkeyup' : 'convertirMayuscula(this);'
            # }),
            # 'seg_mes' : forms.TextInput(attrs={
            #     'class' : 'input-campo', 
            #     'id' : 'doc_nombres',
            #     'onkeypress' : 'return soloLetras(event);',
            #     'onkeyup' : 'convertirMayuscula(this);'
            # }),
            'seg_fecha' : forms.DateInput(attrs={
                'class' : 'form-control datepicker input-campo', 
                'id' : 'per_inicio',
            }),
        }