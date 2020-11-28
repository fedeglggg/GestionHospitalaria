from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime
from django.db import models
from .models import Especialidad, Doctor, TipoEstudio, Turno, Paciente

# los fields se usan en el is_valid() matcheandolos con los names de los input 
# no se usa los id_nombredefield ej id_username para algo, no recuerdo -> chequear esto dsp

class SignUpFormMedico(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    matricula = forms.CharField(max_length=32)
    
    # al postear los checkboxes si no esta lleno no lo manda directamente, por eso required false
    traumatologia = forms.BooleanField(required = False)
    clinica_medica = forms.BooleanField(required = False)
    cardiologia = forms.BooleanField(required = False)
    dermatologia = forms.BooleanField(required = False)
    oftalmologia = forms.BooleanField(required = False)
    endocrinologia = forms.BooleanField(required = False)
    ginecologia = forms.BooleanField(required = False)
    obstetricia = forms.BooleanField(required = False)
    psicologia = forms.BooleanField(required = False)
    diagnostico_por_imagenes = forms.BooleanField(required = False)
    nutricion = forms.BooleanField(required = False)
    pediatria = forms.BooleanField(required = False)
    psiquiatria = forms.BooleanField(required = False)
    neumonologia = forms.BooleanField(required = False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'matricula', 
        'traumatologia',
        'clinica_medica',
        'cardiologia',
        'dermatologia',
        'oftalmologia',
        'endocrinologia',
        'ginecologia',
        'obstetricia',
        'psicologia',
        'diagnostico_por_imagenes',
        'nutricion',
        'pediatria',
        'psiquiatria',
        'neumonologia',
        'password1', 'password2')

class SignUpFormPaciente(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    dni = forms.IntegerField()
    date_of_birth = forms.DateField()
    obra_social = forms.CharField(max_length=32)
    phone_number  = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number' , 'dni', 'obra_social', 'date_of_birth', 'email', 'password1', 'password2')

# para que pase el .is_valid()
class CreateFormTurno(ModelForm):
    tipo_estudio_name = forms.CharField(max_length=30)
    doctor_name = forms.CharField(max_length=30)
    paciente_name = forms.CharField(max_length=30)
    date = forms.DateField(required=True)
    #timeFrom = forms.ChoiceField(choices=horarios, required=True, label="Seleccione su horario")
    timeFrom = forms.TimeField(required=True)
    #timeTo = forms.TimeField(required=True)

    class Meta:
        model = Turno
        fields = ('tipo_estudio_name', 'doctor_name', 'date', 'timeFrom')

# si usas ModelForm chequea que sea el unico existente en la bd con el is_valid() en la view
class EspecialidadForm(forms.Form):
    name = forms.CharField(max_length=100, help_text="Ingrese el nombre de la especialidad (p. ej. Neurología, Traumatología etc.)")
    class Meta:
        model = Especialidad
        fields = ('name',)

class DoctorNameForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    class Meta:
        model = User
        fields = ('first_name','last_name',)

class DoctorMatriculaForm(forms.Form):
    matricula = forms.CharField(max_length=32)
    especialidad = forms.CharField(max_length=32)
    class Meta:
        model = Doctor
        fields = ('matricula', 'especialidad')

class TurnoDateForm(forms.Form):
    date = forms.DateField()
    dni = forms.IntegerField()
    class Meta:
        model = Turno
        fields = ('date', 'dni')

class TurnoDateForm2(forms.Form):
    date = forms.DateField()
    class Meta:
        model = Turno
        fields = ('date')

class TurnoDateForm3(forms.Form):
    date = forms.DateField()
    timeFrom = forms.TimeField()
    class Meta:
        model = Turno
        fields = ('date','timeFrom',)

class DNIForm(forms.Form):
    dni = forms.IntegerField()
    class Meta:
        model = Paciente
        fields = ('dni')

class CreateFormTurno33(ModelForm):
    tipo_estudio_name = forms.CharField(max_length=30)
    doctor_name = forms.CharField(max_length=30)
    date = forms.DateField(required=True)
    timeFrom = forms.TimeField(required=True)
    #timeTo = forms.TimeField(required=True)

    class Meta:
        model = Turno
        fields = ('tipo_estudio_name', 'doctor_name', 'date', 'timeFrom')


