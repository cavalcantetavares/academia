# gestao_academia/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse

from .models import (
    Modalidade, Aluno, Plano, Faixa, 
    Turma, Matricula, Instrutor, Pagamento, Horario
)
from .forms import (
    ModalidadeForm, AlunoForm, MatriculaForm, 
    PagamentoForm, InstrutorForm, TurmaForm
)

@login_required
def dashboard(request):
    print("\n--- INICIANDO TESTE DE DEPURAÇÃO NO DASHBOARD ---")
    
    # --- Mude o número 3 para o ID de uma modalidade que você SABE que tem turmas registadas ---
    modalidade_id_teste = 3 
    print(f"A procurar turmas para a modalidade com ID: {modalidade_id_teste}")
    
    # Executamos a mesma query que a nossa view AJAX faz
    turmas_encontradas = Turma.objects.filter(modalidade_id=modalidade_id_teste)
    
    print(f"Query executada: Turma.objects.filter(modalidade_id={modalidade_id_teste})")
    print(f"Resultado (QuerySet): {turmas_encontradas}")
    print(f"Número de turmas encontradas: {turmas_encontradas.count()}")
    
    if turmas_encontradas.exists():
        print("Turmas encontradas:")
        for turma in turmas_encontradas:
            print(f"  - Turma ID {turma.id}: {str(turma)}")
    else:
        print("Nenhuma turma encontrada para esta modalidade.")

    print("--- FIM DO TESTE DE DEPURAÇÃO ---\n")
    
    # O resto do código do dashboard continua igual para a página carregar
    total_alunos = Aluno.objects.count()
    total_planos = Plano.objects.count()
    total_modalidades = Modalidade.objects.count()
    ultimos_alunos = Aluno.objects.order_by('-data_matricula')[:5]
    hoje = date.today()
    dia_semana_hoje = hoje.isoweekday() 
    turmas_hoje = Turma.objects.filter(horarios__dia_da_semana=dia_semana_hoje).distinct().order_by('horarios__horario_inicio')

    contexto = {
        'total_alunos': total_alunos,
        'total_planos': total_planos,
        'total_modalidades': total_modalidades,
        'ultimos_alunos': ultimos_alunos,
        'turmas_hoje': turmas_hoje,
        'alunos_pendentes': [], # Apenas para evitar erros no template
        'receita_mes_atual': 0, # Apenas para evitar erros no template
        'titulo': 'Dashboard de Teste'
    }
    return render(request, 'gestao_academia/dashboard.html', contexto)
# --- CRUD PARA MODALIDADES ---
@login_required
def lista_modalidades(request):
    modalidades = Modalidade.objects.all()
    return render(request, 'gestao_academia/lista_modalidades.html', {'modalidades': modalidades})

@login_required
def criar_modalidade(request):
    if request.method == 'POST':
        form = ModalidadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modalidade criada com sucesso!')
            return redirect('lista_modalidades')
    else:
        form = ModalidadeForm()
    return render(request, 'gestao_academia/modalidade_form.html', {'form': form, 'titulo': 'Criar Nova Modalidade'})

@login_required
def editar_modalidade(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    if request.method == 'POST':
        form = ModalidadeForm(request.POST, instance=modalidade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modalidade atualizada com sucesso!')
            return redirect('lista_modalidades')
    else:
        form = ModalidadeForm(instance=modalidade)
    return render(request, 'gestao_academia/modalidade_form.html', {'form': form, 'titulo': 'Editar Modalidade', 'modalidade': modalidade})

@login_required
def apagar_modalidade(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    if request.method == 'POST':
        modalidade.delete()
        messages.success(request, 'Modalidade apagada com sucesso!')
        return redirect('lista_modalidades')
    return render(request, 'gestao_academia/modalidade_confirm_delete.html', {'modalidade': modalidade})


# --- CRUD PARA ALUNOS ---
@login_required
def lista_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, 'gestao_academia/aluno_lista.html', {'alunos': alunos})

@login_required
def aluno_detalhe(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'gestao_academia/aluno_detalhe.html', {'aluno': aluno})

@login_required
def aluno_criar(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno criado com sucesso!')
            return redirect('lista_alunos')
    else:
        form = AlunoForm()
    return render(request, 'gestao_academia/aluno_form.html', {'form': form, 'titulo': 'Criar Aluno'})

@login_required
def aluno_editar(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('lista_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'gestao_academia/aluno_form.html', {'form': form, 'titulo': 'Editar Aluno'})

@login_required
def aluno_apagar(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno apagado com sucesso!')
        return redirect('lista_alunos')
    return render(request, 'gestao_academia/aluno_confirm_delete.html', {'aluno': aluno})


# --- CRUD PARA INSTRUTORES ---
@login_required
def lista_instrutores(request):
    instrutores = Instrutor.objects.all()
    return render(request, 'gestao_academia/instrutor_lista.html', {'instrutores': instrutores})

@login_required
def instrutor_criar(request):
    if request.method == 'POST':
        form = InstrutorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instrutor registado com sucesso!')
            return redirect('lista_instrutores')
    else:
        form = InstrutorForm()
    return render(request, 'gestao_academia/instrutor_form.html', {'form': form, 'titulo': 'Registar Novo Instrutor'})

@login_required
def instrutor_editar(request, pk):
    instrutor = get_object_or_404(Instrutor, pk=pk)
    if request.method == 'POST':
        form = InstrutorForm(request.POST, instance=instrutor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do instrutor atualizados com sucesso!')
            return redirect('lista_instrutores')
    else:
        form = InstrutorForm(instance=instrutor)
    return render(request, 'gestao_academia/instrutor_form.html', {'form': form, 'titulo': 'Editar Instrutor'})

@login_required
def instrutor_apagar(request, pk):
    instrutor = get_object_or_404(Instrutor, pk=pk)
    if request.method == 'POST':
        instrutor.delete()
        messages.success(request, 'Instrutor apagado com sucesso!')
        return redirect('lista_instrutores')
    return render(request, 'gestao_academia/instrutor_confirm_delete.html', {'instrutor': instrutor})


# --- CRUD PARA TURMAS E HORÁRIOS ---
@login_required
def grade_horarios(request):
    # Buscamos todas as turmas e usamos 'prefetch_related' para carregar
    # todos os seus horários de uma forma eficiente, evitando múltiplas queries.
    turmas = Turma.objects.prefetch_related('horarios').order_by('nome')

    contexto = {
        'turmas': turmas,
        'titulo': 'Grade de Horários'
    }
    return render(request, 'gestao_academia/grade_horarios.html', contexto)


@login_required
def turma_criar(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma criada com sucesso!')
            return redirect('grade_horarios')
    else:
        form = TurmaForm()
    return render(request, 'gestao_academia/turma_form.html', {'form': form, 'titulo': 'Criar Nova Turma'})

@login_required
def turma_editar(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('grade_horarios')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'gestao_academia/turma_form.html', {'form': form, 'titulo': 'Editar Turma'})

@login_required
def turma_apagar(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        turma.delete()
        messages.success(request, 'Turma apagada com sucesso!')
        return redirect('grade_horarios')
    return render(request, 'gestao_academia/turma_confirm_delete.html', {'turma': turma})


# --- CRUD PARA MATRÍCULAS ---
@login_required
def matricula_criar(request, aluno_pk):
    aluno = get_object_or_404(Aluno, pk=aluno_pk)
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.aluno = aluno
            matricula.save()
            messages.success(request, 'Aluno matriculado na turma com sucesso!')
            return redirect('aluno_detalhe', pk=aluno.pk)
    else:
        form = MatriculaForm()

    return render(request, 'gestao_academia/matricula_form.html', {'form': form, 'aluno': aluno})

@login_required
def matricula_editar(request, pk):
    matricula = get_object_or_404(Matricula, pk=pk)
    if request.method == 'POST':
        form = MatriculaForm(request.POST, instance=matricula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matrícula atualizada com sucesso!')
            return redirect('aluno_detalhe', pk=matricula.aluno.pk)
    else:
        form = MatriculaForm(instance=matricula)
    return render(request, 'gestao_academia/matricula_form.html', {'form': form, 'aluno': matricula.aluno})

@login_required
def matricula_apagar(request, pk):
    matricula = get_object_or_404(Matricula, pk=pk)
    aluno_pk = matricula.aluno.pk
    if request.method == 'POST':
        matricula.delete()
        messages.success(request, 'Matrícula apagada com sucesso!')
        return redirect('aluno_detalhe', pk=aluno_pk)
    return render(request, 'gestao_academia/matricula_confirm_delete.html', {'matricula': matricula})


# --- VIEWS DE PAGAMENTOS ---
@login_required
def lista_pagamentos(request):
    pagamentos = Pagamento.objects.all()
    return render(request, 'gestao_academia/pagamento_lista.html', {'pagamentos': pagamentos})

@login_required
def registar_pagamento(request, aluno_pk):
    aluno = get_object_or_404(Aluno, pk=aluno_pk)
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.aluno = aluno
            pagamento.save()
            messages.success(request, 'Pagamento registado com sucesso!')
            return redirect('aluno_detalhe', pk=aluno.pk)
    else:
        form = PagamentoForm(initial={'valor': aluno.plano.valor if aluno.plano else 0})
    return render(request, 'gestao_academia/pagamento_form.html', {'form': form, 'aluno': aluno})

def pagamento_apagar(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    aluno_pk = pagamento.aluno.pk
    if request.method == 'POST':
        pagamento.delete()
        messages.success(request, 'Pagamento apagado com sucesso!')
        return redirect('aluno_detalhe', pk=aluno_pk)
    return render(request, 'gestao_academia/pagamento_confirm_delete.html', {'pagamento': pagamento})


# --- VIEWS AUXILIARES PARA AJAX ---
def carregar_opcoes_matricula(request):
    turma_id = request.GET.get('turma_id')
    faixas = Faixa.objects.none()
    if turma_id:
        try:
            turma = Turma.objects.get(pk=turma_id)
            if turma.modalidade.utiliza_faixas:
                faixas = Faixa.objects.filter(modalidade=turma.modalidade)
        except Turma.DoesNotExist:
            pass
    
    return JsonResponse(list(faixas.values('id', 'nome')), safe=False)
def carregar_turmas(request):
    modalidade_id = request.GET.get('modalidade_id')
    turmas = Turma.objects.filter(modalidade_id=modalidade_id).order_by('nome')
    return JsonResponse(list(turmas.values('id', 'nome')), safe=False)

def carregar_faixas(request):
    modalidade_id = request.GET.get('modalidade_id')
    faixas = Faixa.objects.filter(modalidade_id=modalidade_id).order_by('ordem')
    return JsonResponse(list(faixas.values('id', 'nome')), safe=False)