# gestao_academia/forms.py
from django import forms
from datetime import date
from .models import (
    Modalidade, Aluno, Plano, Faixa, 
    Turma, Matricula, Instrutor, Pagamento, Horario
)

class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        fields = ['nome', 'descricao', 'utiliza_faixas']

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        exclude = ['turmas']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
        }

class InstrutorForm(forms.ModelForm):
    class Meta:
        model = Instrutor
        fields = '__all__'

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = '__all__'

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['valor', 'data_pagamento', 'mes_referencia', 'forma_pagamento']
        widgets = {
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
            'mes_referencia': forms.DateInput(attrs={'type': 'date'}),
        }

# --- FORMULÁRIO DE MATRÍCULA CORRIGIDO ---
class MatriculaForm(forms.ModelForm):
    # Adicionamos um campo extra que não está no modelo, apenas para filtrar.
    modalidade = forms.ModelChoiceField(
        queryset=Modalidade.objects.all(),
        label="Modalidade",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_modalidade'})
    )

    class Meta:
        model = Matricula
        # A 'modalidade' não está aqui porque não é um campo do modelo Matricula.
        fields = ['turma', 'faixa']
        widgets = {
            'turma': forms.Select(attrs={'class': 'form-select', 'id': 'id_turma'}),
            'faixa': forms.Select(attrs={'class': 'form-select', 'id': 'id_faixa'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turma'].queryset = Turma.objects.none()
        self.fields['faixa'].queryset = Faixa.objects.none()

        # Se o formulário for submetido (POST), precisamos de preencher os querysets
        # para que a validação funcione.
        if 'modalidade' in self.data:
            try:
                modalidade_id = int(self.data.get('modalidade'))
                self.fields['turma'].queryset = Turma.objects.filter(modalidade_id=modalidade_id).order_by('nome')
                self.fields['faixa'].queryset = Faixa.objects.filter(modalidade_id=modalidade_id).order_by('ordem')
            except (ValueError, TypeError):
                pass
        # Se estivermos a editar uma instância existente, também preenchemos os querysets.
        elif self.instance.pk and self.instance.turma:
            self.fields['modalidade'].initial = self.instance.turma.modalidade
            self.fields['turma'].queryset = Turma.objects.filter(modalidade=self.instance.turma.modalidade)
            self.fields['faixa'].queryset = Faixa.objects.filter(modalidade=self.instance.turma.modalidade)
