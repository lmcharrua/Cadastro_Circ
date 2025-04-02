from django.contrib.auth.forms import UserCreationForm
from .models import serv_dados, terminacao
from django import forms
from django.forms.widgets import TextInput, DateInput, ChoiceWidget
from crispy_formset_modal.helper import ModalEditFormHelper
from crispy_formset_modal.layout import ModalEditLayout, ModalEditFormsetLayout
from crispy_forms.helper import FormHelper
from crispy_formset_modal.layout import ModalEditFormsetLayout
from crispy_forms.layout import Column, Fieldset, Layout, Row, Submit

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = ModalEditFormHelper()
        self.helper.layout = ModalEditLayout(
            "Local",
            "Equipamento",
            "SAP",
            "Notas",
        )

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

class DadosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("ISID"), Column("ISID_name")),
            Row(Column("Service_type"),Column("Mux_mode")),
            Row(Column("Connect_type"), Column("VLAN_translation")),
            Row(Column("Cliente"), Column("Service_status")),
            "Notas",
            Fieldset(
                "Terminações",
                ModalEditFormsetLayout(
                    "terminacaoInline",
                    list_display=["Local", "Equipamento", "SAP"],
                ),
            ),
            Submit("submit", "Criar", css_class="btn btn-primary float-right"),
        )

    class Meta:
        model = serv_dados
        fields = "__all__"