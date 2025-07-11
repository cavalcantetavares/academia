# gestao_academia/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # NOVA ROTA PARA O DASHBOARD

    path('dashboard/', views.dashboard, name='dashboard'),



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

     # URL de Matrículas
    path('alunos/<int:aluno_pk>/matricular/', views.matricula_criar, name='matricula_criar'),
    path('matriculas/<int:pk>/editar/', views.matricula_editar, name='matricula_editar'),
    path('matriculas/<int:pk>/apagar/', views.matricula_apagar, name='matricula_apagar'),

    # URLs de Pagamentos
    path('pagamentos/', views.lista_pagamentos, name='lista_pagamentos'),
    path('alunos/<int:aluno_pk>/pagamento/', views.registar_pagamento, name='registar_pagamento'),
    path('pagamentos/<int:pk>/apagar/', views.pagamento_apagar,name='pagamento_apagar'),

    # URLs de Instrutores
    path('instrutores/', views.lista_instrutores, name='lista_instrutores' ),
    path('instrutores/novo/', views.instrutor_criar, name='instrutor_criar'),
    path('instrutores/<int:pk>/editar/', views.instrutor_editar, name='instrutor_editar'),
    path('instrutores/<int:pk>/apagar/', views.instrutor_apagar, name='instrutor_apagar'),

    # URLs de Turmas
    path('horarios/', views.grade_horarios, name='grade_horarios'),
    path('horarios/nova', views.turma_criar, name='turma_criar'),
    path('horarios/<int:pk>/editar/', views.turma_editar, name='turma_editar'),
    path('horarios/<int:pk>/apagar/', views.turma_apagar, name='turma_apagar'),

    # URL para a chamada AJAX
    path('ajax/carregar-turmas/', views.carregar_turmas, name='ajax_carregar_turmas'),
    path('ajax/carregar-faixas/', views.carregar_faixas, name='ajax_carregar_faixas'),

]
