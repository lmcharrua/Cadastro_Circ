from .models import circfoe
from django import forms

class circfoeForm(forms.ModelForm):
    
    class Meta:
        model = circfoe
        fields = "__all__"

class cria_circfoeForm(forms.ModelForm):

    class Meta:
        model = circfoe
        fields = [
            'referencia',
            'encomenda',
            'cliente',
            'dist_km',
            'dist_optica',
            'data_obj',
            'data_entrega',
            'data_ocupa',
            'estado',
            'local_a',
            'ligacao_a',
            'local_b',
            'ligacao_b',
            'observacoes',
        ]
    