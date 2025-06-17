#gestao_academia/forms.py
from django import forms
from .models import Modalidade

class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class' : 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4 })
        }