# gestao_academia/admin.py
from django.contrib import admin
from .models import Modalidade, Plano, Faixa, Aluno, MatriculaModalidade

class MatriculaModalidadeInline(admin.TabularInline):
    model = MatriculaModalidade
    extra = 1

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'email', 'telefone', 'plano','cpf','cidade')
    search_fields = ('nome_completo', 'email','cpf')
    list_filter = ('plano','cidade')
    inlines = [MatriculaModalidadeInline]
     # Cria um "campo" personalizado para a área de admin
    def get_idade_display(self, obj):
       idade = obj.get_idade()
       return f"{idade} anos" if idade is not None else "N/A"
    # Define um nome para a nova coluna
    get_idade_display.short_description = 'Idade'


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'utiliza_faixas')
    list_filter = ('utiliza_faixas',)

admin.site.register(Plano)
admin.site.register(Faixa)