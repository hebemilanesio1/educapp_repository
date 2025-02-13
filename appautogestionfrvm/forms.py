from django import forms
from .models import Curso, Alumno
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields= '__all__'

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',  # Personalizar la etiqueta
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo Electrónico'
        })
    )
    password = forms.CharField(
        label='Contraseña',  # Personalizar la etiqueta
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )


class AlumnoForm(forms.ModelForm):
    TIPO_DOCUMENTO_CHOICES = [
        ('CDI', 'CDI'),
        ('DNI', 'DNI'),
        ('Pasaporte', 'Pasaporte'),
    ]

    tipo_documento = forms.ChoiceField(
        choices=TIPO_DOCUMENTO_CHOICES,
    )

    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        empty_label="Seleccionar Curso",  # Opcional: etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Alumno
        fields = ['curso','apellido', 'nombre', 'tipo_documento', 'numero_documento', 'direccion', 'localidad', 'telefono_fijo', 'telefono_celular', 'email']
        widgets = {
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_fijo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_celular': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class AlumnoSearchForm(forms.Form):
    numero_documento = forms.CharField(max_length=20, required=True)

class BuscarAlumnoForm(forms.Form):
    dniAlumno = forms.CharField(label='Número de DNI', max_length=20)