from tkinter import SEL
from django import forms
from django.core.exceptions import ValidationError
from .models import sdados, sterm

class sdadosForm(forms.ModelForm):
    SERV_TYPE_CHOICES = [
        ('P','Pseudowire'),
        ('S','Switched'),
        ('T','Transparent'),
        ('N','None'),
    ]
    MUX_MODE_CHOICES = [
        ('OTO','One-to-one'),
        ('MTM','Many-to-many'),
        ('N','None')
    ]
    CONN_TYPE_CHOICES = [
        ('PTP','Point-to-point'),
        ('PTMP','Point-to-multipoint'),
        ('MTM','Multipoint-to-multipoint'),
        ('P','Pseudowire'),
        ('N','none')
    ]
    VLAN_TRANS_CHOICES = [
        ('Yes','Yes'),
        ('No','No'),
        ('N','none')
    ]
    SERV_STATUS_CHOICES = [
        ('A','Activo'),
        ('I','Em Configuração'),
        ('D','Desligado')
    ]

    ISID = forms.CharField(
         widget=forms.TextInput(attrs={
            'class': 'input input-bordered',
            'placeholder': 'ISID'
        })
    )

    ISID_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered',
            'placeholder': 'ISID Name'
        })
    )   

    Service_type = forms.ChoiceField(SELectionChoices=SERV_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'input input-bordered',
            'placeholder': 'Service Type'
        }),
        required=False,
        initial='N'
    )  

    Mux_mode = forms.ChoiceField(SELectionChoices=MUX_MODE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'input input-bordered',
            'placeholder': 'Mux Mode'
        }),
        required=T,
        initial='N'
    )   

    Service_status = forms.ChoiceField(SELectionChoices=SERV_STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'input input-bordered',
            'placeholder': 'Estado serviço'
        }),
        required=True,
        initial='I'
    )
    Connect_type = forms.ChoiceField(SELectionChoices=CONN_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'input input-bordered',
            'placeholder': 'Connection Type'
        }),
        required=True,
        initial='N'
    )
    VLAN_translation = forms.ChoiceField(SELectionChoices=VLAN_TRANS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'input input-bordered',
            'placeholder': 'VLAN Translation'
        }),
        required=True,
        initial='N'
    )
    cliente = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered',
            'placeholder': 'Cliente'
        })
    )
    Notas = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input input-bordered',
            'placeholder': 'Notas',
            'rows': 3
        }),
        required=False,
        initial=''
    )

    
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

class stermForm(forms.ModelForm):

    Local = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered',
            'placeholder': 'Local'
        })
    )
    Equipamento = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered',
            'placeholder': 'Equipamento'
        })
    )
    SAP = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered',
            'placeholder': 'SAP'
        })
    )
    Notas = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input input-bordered',
            'placeholder': 'Notas',
            'rows': 3
        }),
        required=False,
        initial=''
    )

    class Meta:
        model = sterm
        fields = [
            'Local',
            'Equipamento',
            'SAP',
            'Notas'
        ]   
