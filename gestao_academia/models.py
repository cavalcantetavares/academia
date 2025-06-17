from django.db import models

class Modalidade(models.Model):
   nome  = models.CharField(max_length=100,unique=True, help_text="Nome da modalidade (Ex: Judô, Jiu Jitsu.)")
   descricao = models.TextField(blank=True,null=True, help_text="Uma breve descrição da modalidade.")

   def __str__(self):
       return self.nome