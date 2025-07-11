# gestao_academia/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from django.core.paginator import Paginator
from django.db.models import Sum
from .models import (
    Modalidade, Aluno, MatriculaModalidade, Plano, 
    Faixa, Instrutor, Turma, Pagamento
)
from .forms import (
    ModalidadeForm, AlunoForm, MatriculaModalidadeForm, 
    PagamentoForm, InstrutorForm, TurmaForm
)
from django.http import JsonResponse

@login_required
def dashboard(request):
    hoje = date.today()

    # --- LÓGICA EXISTENTE ---
    total_alunos = Aluno.objects.count()
    ultimos_alunos = Aluno.objects.order_by('-data_matricula')[:5]
    dia_semana_hoje = hoje.isoweekday() 
    turmas_hoje = Turma.objects.filter(dia_da_semana=dia_semana_hoje).order_by('horario_inicio')

    # --- NOVA LÓGICA FINANCEIRA ---

    # 1. Calcular a receita do mês atual
    receita_mes_atual = Pagamento.objects.filter(
        data_pagamento__year=hoje.year,
        data_pagamento__month=hoje.month
    ).aggregate(Sum('valor'))['valor__sum'] or 0.00

    # 2. Encontrar alunos com mensalidades pendentes para o mês atual
    ids_alunos_pagos = Pagamento.objects.filter(
        mes_referencia__year=hoje.year,
        mes_referencia__month=hoje.month
    ).values_list('aluno_id', flat=True)

    alunos_pendentes = Aluno.objects.exclude(id__in=ids_alunos_pagos).order_by('nome_completo')

    contexto = {
        'total_alunos': total_alunos,
        'ultimos_alunos': ultimos_alunos,
        'turmas_hoje': turmas_hoje,
        'receita_mes_atual': receita_mes_atual, # Nova variável
        'alunos_pendentes': alunos_pendentes,   # Nova variável
        'titulo': 'Dashboard'
    }
    return render(request, 'gestao_academia/dashboard.html', contexto)


# --- VIEWS PARA MODALIDADES ---
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


# --- VIEWS PARA ALUNOS ---
@login_required
def lista_alunos(request):
    alunos = Aluno.objects.select_related('plano').prefetch_related('pagamentos').order_by('nome_completo')
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
            messages.success(request, 'Aluno registado com sucesso!')
            return redirect('lista_alunos')
    else:
        form = AlunoForm()
    return render(request, 'gestao_academia/aluno_form.html', {'form': form, 'titulo': 'Registar Novo Aluno'})

@login_required
def aluno_editar(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do aluno atualizados com sucesso!')
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

# --- VIEW PARA MATRÍCULAS ---
def matricula_criar(request, aluno_pk):
    aluno = get_object_or_404(Aluno, pk=aluno_pk)
    if request.method == 'POST':
        form = MatriculaModalidadeForm(request.POST)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.aluno = aluno
            matricula.save()
            messages.success(request, f'Matrícula em {matricula.modalidade.nome} adicionada com sucesso!')
            return redirect('aluno_detalhe', pk=aluno_pk)
    else:
        form = MatriculaModalidadeForm()

    # A lógica de filtragem dinâmica foi removida daqui, pois agora é desnecessária.

    contexto = {
        'form': form,
        'aluno': aluno,
        'titulo': f'Nova Matrícula para {aluno.nome_completo}'
    }
    return render(request, 'gestao_academia/matricula_form.html', contexto)

@login_required
def matricula_editar(request, pk):
    matricula = get_object_or_404(MatriculaModalidade, pk=pk)
    if request.method == 'POST':
        form = MatriculaModalidadeForm(request.POST, instance=matricula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matrícula atualizada com sucesso!')
            return redirect('aluno_detalhe', pk=matricula.aluno.pk)
    else:
        form = MatriculaModalidadeForm(instance=matricula)

    contexto = {
        'form': form,
        'aluno': matricula.aluno,
        'titulo': f'Editar Matrícula de {matricula.aluno.nome_completo}'
    }
    return render(request, 'gestao_academia/matricula_form.html', contexto)

@login_required
def matricula_apagar(request, pk):
    matricula = get_object_or_404(MatriculaModalidade, pk=pk)
    aluno_pk = matricula.aluno.pk
    if request.method == 'POST':
        matricula.delete()
        messages.success(request, 'Matrícula apagada com sucesso!')
        return redirect('aluno_detalhe', pk=aluno_pk)

    return render(request, 'gestao_academia/matricula_confirm_delete.html', {'matricula': matricula})


# --- VIEWS PARA PAGAMENTOS ---
@login_required
def registar_pagamento(request, aluno_pk):
    aluno = get_object_or_404(Aluno, pk=aluno_pk)
    contexto = {
        'aluno': aluno,
        'titulo': f'Registar Pagamento para {aluno.nome_completo}'
    }
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
    contexto['form'] = form
    return render(request, 'gestao_academia/pagamento_form.html', contexto)

@login_required
def lista_pagamentos(request):
    queryset = Pagamento.objects.all().order_by('-data_pagamento')
    termo_pesquisa = request.GET.get('pesquisa', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    if termo_pesquisa:
        queryset = queryset.filter(aluno__nome_completo__icontains=termo_pesquisa)
    if data_inicio:
        queryset = queryset.filter(data_pagamento__gte=data_inicio)
    if data_fim:
        queryset = queryset.filter(data_pagamento__lte=data_fim)
    paginador = Paginator(queryset, 10)
    pagina_num = request.GET.get('pagina')
    pagina_obj = paginador.get_page(pagina_num)
    contexto = {
        'pagina_obj': pagina_obj, 
        'titulo': 'Histórico de Pagamentos',
        'termo_pesquisa': termo_pesquisa,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'gestao_academia/pagamento_lista.html', contexto)

@login_required
def pagamento_apagar(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    aluno_pk = pagamento.aluno.pk
    if request.method == 'POST':
        pagamento.delete()
        messages.success(request, 'Pagamento apagado com sucesso!')
        return redirect('aluno_detalhe', pk=aluno_pk)
    contexto = {
        'pagamento': pagamento,
        'aluno': pagamento.aluno,
    }
    return render(request, 'gestao_academia/pagamento_confirm_delete.html', contexto)

# --- VIEWS PARA INSTRUTORES ---
@login_required
def lista_instrutores(request):
    instrutores = Instrutor.objects.all().order_by('nome')
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

# --- VIEWS PARA TURMAS/HORÁRIOS ---
@login_required
def grade_horarios(request):
    turmas = Turma.objects.all()
    dias_com_turmas = {}
    for dia_num, dia_nome in Turma.DIAS_SEMANA:
        turmas_do_dia = turmas.filter(dia_da_semana=dia_num)
        if turmas_do_dia:
            dias_com_turmas[dia_nome] = turmas_do_dia
    return render(request, 'gestao_academia/grade_horarios.html', {'dias_com_turmas': dias_com_turmas})

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


# --- NOVA VIEW AUXILIAR PARA AJAX/JAVASCRIPT ---
def carregar_turmas(request):
    modalidade_id = request.GET.get('moalidade_id')
    turmas = Turma.objects.filter(modalidade_id=modalidade_id).order_by('dia_da_semana', 'horario_inicio')

    turmas_lista = []
    for turma in turmas:
        turmas_lista.append({
            'id': turma.id,
            'display': srt(turma) # Usa o __str__ do modelo para um texto descritivo
        })
    return  JsonResponse(turmas_lista, safe=False)    

# --- NOVA VIEW PARA CARREGAR FAIXAS ---
def carregar_faixas(request):
    modalidade_id = request.GET.get('modalidade_id')
    # Busca as faixas que pertencem à modalidade selecionada
    faixas = Faixa.objects.filter(modalidade_id=modalidade_id).order_by('ordem')
    # Formata os dados para serem enviados como JSON
    faixas_list = list(faixas.values('id', 'nome'))
    return JsonResponse(faixas_list, safe=False)
