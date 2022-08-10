from urllib import request
from urllib.request import Request
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ProyectoEleusisApp.models import *
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = '__all__'



class EventoForm(forms.ModelForm):
    descripcion = forms.CharField(label='Descripcion',max_length=500,widget=forms.Textarea(attrs={'rows':'3'}))
    imagen = forms.ImageField(label='Imagen',required=True)
    fecha_inicio = forms.DateField(label='Fecha Inicio(dd/mm/yyyy)')
    hora_inicio = forms.TimeField(label='Hora Inicio(hh:mm:ss)')
    class Meta:
        model = Evento
        fields = '__all__'

class LugarForm(forms.ModelForm):
    nombre = forms.CharField(label='lugar')
    fecha = forms.DateField(label='Fecha Inicio(dd/mm/yyyy)')
    hora = forms.TimeField(label='Hora Inicio(hh:mm:ss)')
    class Meta:
        model = Lugar
        fields = '__all__'

class InscripcionForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre',required=True)
    email = forms.EmailField(label='Email',required=True)
    comprobante = forms.FileField(label='Comprobante de pago',required=True)

    class Meta:
        model = Inscripcion
        fields = ['nombre','email','comprobante']
        
        
