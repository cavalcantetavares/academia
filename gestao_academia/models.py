# gestao_academia/models.py
from django.db import models
from django.utils import timezone

class Modalidade(models.Model):
   nome  = models.CharField(max_length=100,unique=True, help_text="Nome da modalidade (Ex: Judô, Jiu Jitsu.)")
   descricao = models.TextField(blank=True,null=True, help_text="Uma breve descrição da modalidade.")
   utiliza_faixas = models.BooleanField(default=False, verbose_name="Utiliza Faixas?")

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
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF", help_text="Formato: 000.000.000-00", null=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")
    responsavel = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nome do Responsável (se menor de 18 anos)")
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name="CEP")
    rua = models.CharField(max_length=255, blank=True, null=True, verbose_name="Rua")
    numero = models.CharField(max_length=10, blank=True, null=True, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100,blank=True, null=True, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name="Estado (UF)")
    data_matricula = models.DateField(default=timezone.now, verbose_name="Data da Matrícula")
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True, related_name="alunos", verbose_name="Plano Atual")
    foto = models.ImageField(upload_to='fotos_alunos/', blank=True, null=True, verbose_name="Foto")
    modalidades = models.ManyToManyField(Modalidade, through='MatriculaModalidade', related_name="alunos")

    def __str__(self):
        # --- CORREÇÃO ---
        # O erro anterior foi um erro de digitação aqui.
        # O nome do campo é 'nome_completo' (com underscore).
        return self.nome_completo
    
 # --- NOVO MÉTODO PARA CALCULAR A IDADE ---
def get_idade(self):
        print("--- A DEPURAR O MÉTODO get_idade ---") # Linha de Debug 1
        print(f"Aluno: {self.nome_completo}") # Linha de Debug 2
        print(f"Data de Nascimento no DB: {self.data_nascimento}") # Linha de Debug 3
        print(f"Tipo da Data de Nascimento: {type(self.data_nascimento)}") # Linha de Debug 4

        if self.data_nascimento:
            hoje = date.today()
            idade = hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
            print(f"Cálculo da idade: {idade}") # Linha de Debug 5
            return idade

        print("Nenhuma data de nascimento encontrada. A retornar None.") # Linha de Debug 6
        return None # Retorna None se não houver data de nascimento






class MatriculaModalidade(models.Model):
   aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
   modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
   faixa = models.ForeignKey(Faixa, on_delete=models.SET_NULL, null=True, blank=True)
   data_inicio = models.DateField(default=timezone.now)

   class Meta:
      unique_together = ('aluno', 'modalidade')

   def __str__(self):
      return f"{self.aluno.nome_completo} em {self.modalidade.nome}"
