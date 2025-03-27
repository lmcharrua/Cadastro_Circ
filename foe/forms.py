from .models import circfoe
from django import forms

class circfoeForm(forms.ModelForm):
    
    class Meta:
        model = circfoe
        fields = "__all__"

class cria_circfoeForm(forms.ModelForm):

    class Meta:
        model = circfoe
        fields = "__all__"
    