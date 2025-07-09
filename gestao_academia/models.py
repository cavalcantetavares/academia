# gestao_academia/models.py
from django.db import models
from django.utils import timezone
from datetime import date

class Modalidade(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome da modalidade (ex: Musculação, Pilates, Jiu-Jitsu)")
    descricao = models.TextField(blank=True, null=True, help_text="Uma breve descrição da modalidade.")
    utiliza_faixas = models.BooleanField(default=False, verbose_name="Utiliza Faixas?")

    def __str__(self):
        return self.nome

class Instrutor(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Instrutor")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True, verbose_name="E-mail")

    def __str__(self):
        return self.nome

class Plano(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Plano")
    valor = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valor Mensal")
    duracao_meses = models.IntegerField(default=1, verbose_name="Duração (meses)")

    def __str__(self):
        return f"{self.nome} - R${self.valor}/mês"

class Faixa(models.Model):
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE, related_name="faixas")
    nome = models.CharField(max_length=50, verbose_name="Nome da Faixa")
    ordem = models.PositiveIntegerField(help_text="Usado para ordenação (ex: Branca=1, Azul=2, etc.)")

    class Meta:
        unique_together = ('modalidade', 'nome')
        ordering = ['ordem']

    def __str__(self):
        return f"{self.modalidade.nome} - {self.nome}"

class Aluno(models.Model):
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF", help_text="Formato: 000.000.000-00", null=True, blank=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")
    responsavel = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nome do Responsável (se menor de 18 anos)")
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name="CEP")
    rua = models.CharField(max_length=255, blank=True, null=True, verbose_name="Rua")
    numero = models.CharField(max_length=10, blank=True, null=True, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name="Estado (UF)")
    data_matricula = models.DateField(default=timezone.now, verbose_name="Data da Matrícula")
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True, related_name="alunos", verbose_name="Plano Atual")
    foto = models.ImageField(upload_to='fotos_alunos/', blank=True, null=True, verbose_name="Foto")
    modalidades = models.ManyToManyField(Modalidade, through='MatriculaModalidade', related_name="alunos")

    def __str__(self):
        return self.nome_completo

    def get_idade(self):
        if self.data_nascimento:
            hoje = date.today()
            return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return None

    def get_status_mensalidade(self):
        hoje = date.today()
        pagamento_mes_atual = self.pagamentos.filter(
            mes_referencia__year=hoje.year,
            mes_referencia__month=hoje.month
        ).exists()
        if pagamento_mes_atual:
            return "Paga"
        else:
            return "Pendente"
        
 # --- NOVO MÉTODO PARA ENCONTRAR O ÚLTIMO PAGAMENTO ---
    def get_ultimo_mes_pago(self):
        ultimo_pagamento = self.pagamento.order_by('-mes_referencia').first()
        if ultimo_pagamento:
            return ultimo_pagamento.mes_referencia
        return None      

class MatriculaModalidade(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
    faixa = models.ForeignKey(Faixa, on_delete=models.SET_NULL, null=True, blank=True)
    data_inicio = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('aluno', 'modalidade')

    def __str__(self):
        return f"{self.aluno.nome_completo} em {self.modalidade.nome}"

class Pagamento(models.Model):
    FORMAS_PAGAMENTO = [
        ('PIX', 'PIX'), ('DIN', 'Dinheiro'), ('CC', 'Cartão de Crédito'),
        ('CD', 'Cartão de Débito'), ('TRA', 'Transferência Bancária'),
    ]
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="pagamentos")
    valor = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valor Pago")
    data_pagamento = models.DateField(default=timezone.now, verbose_name="Data do Pagamento")
    mes_referencia = models.DateField(verbose_name="Mês de Referência")
    forma_pagamento = models.CharField(max_length=3, choices=FORMAS_PAGAMENTO, verbose_name="Forma de Pagamento")

    class Meta:
        ordering = ['-data_pagamento', '-mes_referencia']

    def __str__(self):
        return f"Pagamento de {self.aluno.nome_completo} - R$ {self.valor} em {self.data_pagamento.strftime('%d/%m/%Y')}"

# --- CORREÇÃO ---
# O erro 'ImportError' foi causado porque a definição da classe Turma estava em falta.
# Adicione a classe abaixo ao seu ficheiro models.py.
class Turma(models.Model):
    DIAS_SEMANA = [
        (1, 'Segunda-feira'),
        (2, 'Terça-feira'),
        (3, 'Quarta-feira'),
        (4, 'Quinta-feira'),
        (5, 'Sexta-feira'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    ]

    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE, related_name="turmas")
    instrutor = models.ForeignKey(Instrutor, on_delete=models.SET_NULL, null=True, blank=True, related_name="turmas")
    dia_da_semana = models.IntegerField(choices=DIAS_SEMANA, verbose_name="Dia da Semana")
    horario_inicio = models.TimeField(verbose_name="Horário de Início")
    horario_fim = models.TimeField(verbose_name="Horário de Fim")
    max_alunos = models.PositiveIntegerField(verbose_name="Máximo de Alunos")

    class Meta:
        ordering = ['dia_da_semana', 'horario_inicio']
        verbose_name = "Turma / Horário"
        verbose_name_plural = "Turmas / Horários"

    def __str__(self):
        return f"{self.modalidade.nome} com {self.instrutor.nome if self.instrutor else 'a definir'} - {self.get_dia_da_semana_display()} ({self.horario_inicio.strftime('%H:%M')}-{self.horario_fim.strftime('%H:%M')})"
