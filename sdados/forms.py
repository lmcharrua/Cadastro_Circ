from django import forms
from .models import sterm, sdados

class StermForm(forms.ModelForm):
    class Meta:
        model = sterm
        fields = "__all__"

class SdadosForm(forms.ModelForm):
    class Meta:
        model = sdados
        fields = "__all__"