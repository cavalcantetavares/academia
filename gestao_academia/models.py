
# gestao_academia/models.py
from django.db import models
from django.utils import timezone
from datetime import date

class Modalidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    utiliza_faixas = models.BooleanField(default=False, verbose_name="Utiliza Faixas?")
    def __str__(self): return self.nome

class Instrutor(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Instrutor")
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    def __str__(self): return self.nome

class Plano(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Plano")
    valor = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valor Mensal")
    duracao_meses = models.IntegerField(default=1, verbose_name="Duração (meses)")
    def __str__(self): return f"{self.nome} - R${self.valor}/mês"

class Faixa(models.Model):
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE, related_name="faixas")
    nome = models.CharField(max_length=50, verbose_name="Nome da Faixa")
    ordem = models.PositiveIntegerField()
    class Meta:
        unique_together = ('modalidade', 'nome')
        ordering = ['ordem']
    def __str__(self): return f"{self.modalidade.nome} - {self.nome}"

class Turma(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Turma")
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE, related_name="turmas")
    instrutor = models.ForeignKey(Instrutor, on_delete=models.SET_NULL, null=True, blank=True, related_name="turmas")
    max_alunos = models.PositiveIntegerField(verbose_name="Máximo de Alunos")
    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
    def __str__(self): return f"{self.nome} ({self.modalidade.nome})"

class Horario(models.Model):
    DIAS_SEMANA = [(1, 'Segunda-feira'), (2, 'Terça-feira'), (3, 'Quarta-feira'), (4, 'Quinta-feira'), (5, 'Sexta-feira'), (6, 'Sábado'), (7, 'Domingo')]
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="horarios")
    dia_da_semana = models.IntegerField(choices=DIAS_SEMANA, verbose_name="Dia da Semana")
    horario_inicio = models.TimeField(verbose_name="Horário de Início")
    horario_fim = models.TimeField(verbose_name="Horário de Fim")
    class Meta:
        ordering = ['dia_da_semana', 'horario_inicio']
        verbose_name = "Horário"
        verbose_name_plural = "Horários"
    def __str__(self): return f"{self.turma.nome} - {self.get_dia_da_semana_display()} ({self.horario_inicio.strftime('%H:%M')})"

class Aluno(models.Model):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    responsavel = models.CharField(max_length=255, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    rua = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    data_matricula = models.DateField(default=timezone.now)
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True, related_name="alunos")
    foto = models.ImageField(upload_to='fotos_alunos/', blank=True, null=True)
    turmas = models.ManyToManyField(Turma, through='Matricula', related_name="alunos")
    def __str__(self): return self.nome_completo

class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    faixa = models.ForeignKey(Faixa, on_delete=models.SET_NULL, null=True, blank=True)
    data_matricula = models.DateField(default=timezone.now)
    class Meta:
        unique_together = ('aluno', 'turma')
    def __str__(self): return f"{self.aluno.nome_completo} na {self.turma.nome}"

class Pagamento(models.Model):
    FORMAS_PAGAMENTO = [('PIX', 'PIX'), ('DIN', 'Dinheiro'), ('CC', 'Cartão de Crédito'), ('CD', 'Cartão de Débito'), ('TRA', 'Transferência Bancária')]
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="pagamentos")
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_pagamento = models.DateField(default=timezone.now)
    mes_referencia = models.DateField()
    forma_pagamento = models.CharField(max_length=3, choices=FORMAS_PAGAMENTO)
    class Meta: ordering = ['-data_pagamento']
    def __str__(self): return f"Pagamento de {self.aluno.nome_completo} - R${self.valor}"
