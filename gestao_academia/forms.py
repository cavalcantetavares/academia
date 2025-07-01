# gestao_academia/forms.py
from django import forms
from datetime import date
# Importações corretas dos modelos necessários
from .models import Modalidade, Aluno, Plano, Faixa, MatriculaModalidade
from .models import Pagamento
from .models import Instrutor, Turma



class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
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
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_nascimento = cleaned_data.get("data_nascimento")
        responsavel = cleaned_data.get("responsavel")

        if data_nascimento:
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
            if idade < 18 and not responsavel:
                self.add_error('responsavel', 'O nome do responsável é obrigatório para menores de 18 anos.')
        return cleaned_data

class MatriculaModalidadeForm(forms.ModelForm):
    faixa = forms.ModelChoiceField(
        queryset=Faixa.objects.all().order_by('modalidade__nome', 'ordem'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Faixa"
    )

    class Meta:
        model = MatriculaModalidade
        fields = ['modalidade', 'faixa']
        widgets = {
            'modalidade': forms.Select(attrs={'class': 'form-select'}),
        }

# NOVO FORMULÁRIO PARA PAGAMENTOS
class PagamentoForm(forms.ModelForm):
    mes_referencia = forms.DateField(
        label="Mês de Referência",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    data_pagamento = forms.DateField(
        label = "Data do Pagamento",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = Pagamento
        fields = ['valor', 'mes_referencia', 'data_pagamento', 'forma_pagamento']
        widgets = {
            'valor': forms.NumberInput(attrs={'class': 'form_pagamento'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-select'}),
        }

# NOVO FORMULÁRIO PARA INSTRUTORES
class InstrutorForm(forms.ModelForm):
    class Meta:
        model = Instrutor
        fields = ['nome', 'email', 'telefone']
        widgets = {
            'nome' : forms.TextInput(attrs={'class': 'form-control'}),
            'telefone' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
        }        
# NOVO FORMULÁRIO PARA TURMAS
class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['modalidade', 'instrutor', 'dia_da_semana', 'horario_inicio', 'horario_fim', 'max_alunos']
        widgets = {
            'modalidade' :  forms.Select(attrs={'class': 'form-select'}),
            'instrutor' : forms.Select(attrs={'class': 'form-select'}),
            'dia_da_semana' : forms.Select(attrs={'class': 'form-select'}),
            'horario_inicio' : forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'horario_fim' : forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'max_alunos' : forms.NumberInput(attrs={'class': 'form-control'}),

        }


