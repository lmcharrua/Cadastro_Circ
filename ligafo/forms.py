from django.contrib.auth.forms import UserCreationForm
from .models import ligafo
from django import forms
from django.forms.widgets import TextInput, DateInput, ChoiceWidget

class LigafoForm(forms.ModelForm):

    class Meta:
        model = ligafo
        fields = "__all__"

class criarligafoForm(forms.ModelForm):
    class Meta:
        model = ligafo
        fields = ['referencia',
                  'cliente',
                  'encomenda',
                  'dist_iet',
                  'dist_optica',
                  'data_pedido',
                  'data_entrega',
                  'estado',
                  'local_a',
                  'equipa_a',
                  'slot_a',
                  'porta_a',
                  'local_b',
                  'equipa_b',
                  'slot_b',
                  'porta_b',
                  'observacoes',
        ]