from django.contrib.auth.forms import UserCreationForm
from .models import serv_dados, terminacao
from django import forms
from django.forms.widgets import TextInput, DateInput, ChoiceWidget

class ServDadosForm(forms.ModelForm):
    class Meta:
        model = serv_dados
        fields = "__all__"

class criarservdadosForm(forms.ModelForm):
    class Meta:
        model = serv_dados
        fields = ['ISID',
                  'ISID_name',
                  'Service_type',
                  'Mux_mode',
                  'Service_status',
                  'Connect_type',
                  'VLAN_translation',
                  'Cliente',
                  'Notas',
        ]
class terminacaoForm(forms.ModelForm):
    class Meta:
        model = terminacao
        fields = "__all__"

class criarterminacaoForm(forms.ModelForm):
    class Meta:
        model = terminacao
        fields = ['main_isid',
                  'Local',
                  'Morada',
                  'Cod_Postal',
                  'dicofre',
                  'Equipamento',
                  'SAP',
                  'Notas',
        ]