from django.contrib.auth.forms import UserCreationForm
from .models import ligafo
from django import forms
from django.forms.widgets import TextInput, DateInput, ChoiceWidget

class LigafoForm(forms.ModelForm):

    class Meta:
        model = ligafo
        fields = "__all__"