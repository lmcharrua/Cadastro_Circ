from tkinter import SEL
from django import forms
from django.core.exceptions import ValidationError
from .models import sdados, sterm

class sdadosForm(forms.ModelForm):
    class Meta:
        model = sdados
        fields = '__all__'

class stermForm(forms.ModelForm):

    class Meta:
        model = sterm
        fields = [
            'misid',
            'Local',
            'Equipamento',
            'SAP',
            'Notas'
        ]   
class stermCreateForm(forms.ModelForm):
       class Meta:
        model = sterm
        fields = [
            'misid',
            'Local',
            'Morada',
            'Cod_Postal',
            'Equipamento',
            'SAP',
            'Notas'
        ]   

class stermEditForm(forms.ModelForm):
       class Meta:
        model = sterm
        fields = [
            'misid',
            'Local',
            'Morada',
            'Cod_Postal',
            'Equipamento',
            'SAP',
            'Notas'
        ]   

