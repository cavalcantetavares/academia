# gestao_academia/models.py
from django.db import models
from django.utils import timezone #Para usar a data atual


class Modalidade(models.Model):
   nome  = models.CharField(max_length=100,unique=True, help_text="Nome da modalidade (Ex: Judô, Jiu Jitsu.)")
   descricao = models.TextField(blank=True,null=True, help_text="Uma breve descrição da modalidade.")
   utiliza_faixas = models.BooleanField(default=False, verbose_name="Utiliza Faixas") 

   def __str__(self):
       return self.nome
   
# NOV MODELO : PLANO
class Plano(models.Model):
   nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Plano")
   valor = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valor Mensal")
   duracao_meses = models.IntegerField(default=1, verbose_name="Duração (meses)") 
    
   def __str__(self):
       return f"{self.nome} - R${self.valor}/mês"
   
# NOVO MODELO: FAIXA
class Faixa(models.Model):
   modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE, related_name="faixas")
   name = models.CharField(max_length=50, verbose_name="Nome da Faixa")
   ordem = models.PositiveIntegerField(help_text="Usado para ordenação (ex: Branca=1, Azul=2, etc.)")
     
   class Meta:
    # Garante que não há faixas com o mesmo nome para a mesma modalidade
       unique_together = ('modalidade', 'name')
       ordering = ['ordem']

   def __str__(self):
     return f"{self.modalidade.name} - {self.name}"
# NOVO MODELO: ALUNO
class Aluno(models.Model):
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")
    data_matricula = models.DateField(default=timezone.now, verbose_name="Data da Matrícula")
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True, related_name="alunos", verbose_name="Plano Atual")
    foto = models.ImageField(upload_to='fotos_alunos/', blank=True, null=True, verbose_name="Foto")
    modalidades = models.ManyToManyField(Modalidade, through='MatriculaModalidade', related_name="alunos")

    def __str__(self):
        return self.name_completo

# NOVO MODELO: MatrículaModalidade (Tabela Intermediária)
# Esta tabela especial liga um Aluno a uma Modalidade e guarda a Faixa do aluno NESSA modalidade específica.
 
class MatriculaModalidade(models.Model):
   aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
   modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
   faixa = models.ForeignKey(Faixa, on_delete=models.SET_NULL, null=True, blank=True)
   data_inicio = models.DateField(default=timezone.now)


   class Meta:
      unique_together = ('aluno', 'modalidade')  # Um aluno só pode se matricular uma vez em cada modalidade

   def __str__(self):
      return f"{self.aluno.nome_completo} em {self.modalidade.nome}"      