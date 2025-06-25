#gestao_academia/forms.py
from django import forms
from .models import Modalidade, Aluno # Adicione Aluno à importação

class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class' : 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4 }),
        }
# NOVO FORMULÁRIO PARA ALUNOS
class AlunoForm(forms.ModelForm):
    # Usamos um widget específico para a data para que o navegador mostre um calendário
    data_nascimento = forms.DateField(
        label = "Data de Nascimento",
        widget = forms.DateInput(attrs={'type': 'date', 'class' : 'form-control'})
    )
    class Meta:
        model = Aluno
        fields = ['nome_completo' ,'data_nascimento', 'email', 'telefone', 'plano', 'foto']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'plano': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }