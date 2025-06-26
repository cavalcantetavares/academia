# gestao_academia/forms.py
from django import forms
from datetime import date
from .models import Modalidade, Aluno, Plano, Faixa, MatriculaModalidade

class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# NOVO FORMULÁRIO PARA ALUNOS (COM CORREÇÃO)
class AlunoForm(forms.ModelForm):
  

    class Meta:
        model = Aluno
        # Adicione 'cpf' e 'responsavel' à lista de campos
        fields = ['nome_completo', 'cpf', 'data_nascimento', 'responsavel', 'telefone', 'email', 'plano', 'foto', 'cep', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'plano': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'id': 'cep'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'id': 'rua'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'id': 'bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'id': 'cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'id': 'uf'}),
        }

    # --- LÓGICA DE VALIDAÇÃO PERSONALIZADA ---
    def clean(self):
        # Pega todos os dados já validados do formulário
        cleaned_data = super().clean()
        data_nascimento = cleaned_data.get("data_nascimento")
        responsavel = cleaned_data.get("responsavel")

        if data_nascimento:
            # Calcula a idade do aluno
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

            # Se for menor de 18 e o campo responsável estiver vazio, gera um erro
            if idade < 18 and not responsavel:
                self.add_error('responsavel', 'O nome do responsável é obrigatório para menores de 18 anos.')

        return cleaned_data