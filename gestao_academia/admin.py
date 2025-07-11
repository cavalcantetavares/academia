# gestao_academia/admin.py
from django.contrib import admin
# Garanta que todos os modelos estão a ser importados
from .models import Modalidade, Plano, Faixa, Aluno, MatriculaModalidade, Instrutor, Turma

class MatriculaModalidadeInline(admin.TabularInline):
    model = MatriculaModalidade
    extra = 1

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'email', 'telefone', 'plano')
    search_fields = ('nome_completo', 'email')
    list_filter = ('plano',)
    inlines = [MatriculaModalidadeInline]

@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'utiliza_faixas')
    list_filter = ('utiliza_faixas',)

# --- CORREÇÃO ---
# Adicionamos o registo de Instrutor e Turma que estava em falta.
admin.site.register(Plano)
admin.site.register(Faixa)
admin.site.register(Instrutor)
admin.site.register(Turma)