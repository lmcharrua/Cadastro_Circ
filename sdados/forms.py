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