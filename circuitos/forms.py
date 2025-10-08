from django.contrib.auth.forms import UserCreationForm
from .models import Circuitos
from django import forms
from django.forms.widgets import TextInput, DateInput, ChoiceWidget

class CreateCircuitoForm(forms.ModelForm):
    class Meta:
        model = Circuitos
        fields = ['N_Circuito', 
                  'Data_Rate', 
                  'Data_Inst', 
                  'Estado_Cct', 
                  'Entidade_PTR1', 
                  'Morada_PTR1', 
                  'Cod_Post_PTR1',
                  'Interface_PTR1',
                  'Equip_PTR1',
                  'Slot_PTR1',
                  'Trib_PTR1',
                  'Entidade_PTR2', 
                  'Morada_PTR2', 
                  'Cod_Post_PTR2',
                  'Interface_PTR2',
                  'Equip_PTR2',
                  'Slot_PTR2',
                  'Trib_PTR2',
                  'User_Cct',
                  'Propriedade_Cct',
                  'Outras_Ref',
                  ]
        
class CircuitoForm(forms.ModelForm):
    class Meta:
        model = Circuitos
        fields = "__all__"

