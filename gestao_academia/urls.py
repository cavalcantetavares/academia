# gestao_academia/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URLs de Modalidades
    path('modalidades/', views.lista_modalidades, name='lista_modalidades'),
    path('modalidades/nova/', views.criar_modalidade, name='criar_modalidade'),
    path('modalidades/<int:pk>/editar/', views.editar_modalidade, name='editar_modalidade'),
    path('modalidades/<int:pk>/apagar/', views.apagar_modalidade, name='apagar_modalidade'),

    # URLs de Alunos
    path('alunos/', views.lista_alunos, name='lista_alunos'),
    path('alunos/novo/', views.aluno_criar, name='aluno_criar'),
    path('alunos/<int:pk>/', views.aluno_detalhe, name='aluno_detalhe'),
    path('alunos/<int:pk>/editar/', views.aluno_editar, name='aluno_editar'),
    path('alunos/<int:pk>/apagar/', views.aluno_apagar, name='aluno_apagar'),
]
