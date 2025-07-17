# gestao_academia/admin.py
from django.contrib import admin
# CORREÇÃO: O nome do modelo mudou de MatriculaModalidade para Matricula
from .models import Modalidade, Plano, Faixa, Aluno, Instrutor, Turma, Horario, Matricula

# Define que os Horários podem ser editados na mesma página da Turma
class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1 # Mostra 1 campo de horário vazio por defeito

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'modalidade', 'instrutor')
    list_filter = ('modalidade', 'instrutor')
    inlines = [HorarioInline] # Adiciona os horários à página da turma

class MatriculaInline(admin.TabularInline):
    model = Matricula
    extra = 1

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'email', 'plano')
    search_fields = ('nome_completo', 'email')
    inlines = [MatriculaInline]

# Registos simples para os outros modelos
admin.site.register(Modalidade)
admin.site.register(Plano)
admin.site.register(Faixa)
admin.site.register(Instrutor)
