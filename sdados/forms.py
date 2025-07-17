""" from tkinter import SEL
from django import forms
from django.core.exceptions import ValidationError
from .models import sdados, sterm

class sdadosForm(forms.ModelForm):
    class Meta:
        model = sdados
        fields = '__all__'

class sdadosCreateForm(forms.ModelForm):
    class Meta:
        model = sdados
        fields = [
            'ISID',
            'ISID_name',
            'Service_type',
            'Mux_mode',
            'Service_status',
            'Connect_type',
            'VLAN_translation',
            'Cliente',
            'Notas'
        ]

class sdadosEditForm(forms.ModelForm):
    class Meta:
        model = sdados
        fields = [
            'ISID',
            'ISID_name',
            'Service_type',
            'Mux_mode',
            'Connect_type',
            'VLAN_translation',
            'Service_status',
            'Cliente',
            'Notas'
        ]

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

 """

from django import forms
from .models import sterm, sdados

class StermForm(forms.ModelForm):
    class Meta:
        model = sterm
        exclude = ['misid']

class SdadosForm(forms.ModelForm):
    class Meta:
        model = sdados
        fields = '__all__'