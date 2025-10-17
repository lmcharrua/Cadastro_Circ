from django.contrib.auth.forms import UserCreationForm
from .models import Circuitos
from django import forms
from django.forms.widgets import TextInput, DateInput, ChoiceWidget

class CreateCartasForm(forms.ModelForm):
    class Meta:
        model = Cartas
        fields = ['fabricante',
                    'data_rececao',
                    'b_type',
                    'part_number',
                    'serial_number',
                    'descricao',
                    'estado',
                    'projeto',
                    'sistema',
                    'localizacao',
                    'equipamento',
                    'subrack',
                    'slot',
                    'porto',
                    'observacoes'
                  ]
        
class CartaForm(forms.ModelForm):
    class Meta:
        model = Cartas
        fields = "__all__"