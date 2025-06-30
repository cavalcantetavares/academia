# gestao_academia/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Modalidade, Aluno, MatriculaModalidade, Plano, Faixa # Importações dos modelos
from .forms import ModalidadeForm, AlunoForm, MatriculaModalidadeForm # Importações dos formulários
from .models import Pagamento
from .forms import PagamentoForm
from django.core.paginator import Paginator
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
    return render(request, 'gestao_academia/modalidade_form.html', {'form': form})

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
    return render(request, 'gestao_academia/modalidade_form.html', {'form': form, 'modalidade': modalidade})

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
    alunos = Aluno.objects.all().order_by('nome_completo')
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
@login_required
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
    
    modalidades_atuais_pks = aluno.matriculamodalidade_set.values_list('modalidade__pk', flat=True)
    form.fields['modalidade'].queryset = Modalidade.objects.exclude(pk__in=modalidades_atuais_pks)

    contexto = {
        'form': form,
        'aluno': aluno,
        'titulo': f'Nova Matrícula para {aluno.nome_completo}'
    }
    return render(request, 'gestao_academia/matricula_form.html', contexto)

# --- NOVA VIEW PARA O DASHBOARD ---

@login_required
def dashboard(request):
    # Calcula as estatísticas
    total_alunos = Aluno.objects.count()
    total_planos = Plano.objects.count()
    total_modalidade = Modalidade.objects.count()
  
    # Busca os últimos 5 alunos registrados
    ultimos_alunos = Aluno.objects.order_by('-data_matricula')[:5]

    contexto = {
        'total_alunos' : total_alunos,
        'total_planos' : total_planos,
        'total_modalidades' : total_modalidade,
        'ultimos_alunos' : ultimos_alunos,
        'titulo' : 'Dashboard'
    }
    return render(request, 'gestao_academia/dashboard.html', contexto)

# --- VIEWS PARA PAGAMENTOS ---
def registar_pagamento(request, aluno_pk):
    aluno = get_object_or_404(Aluno, pk=aluno_pk)

    # --- CORREÇÃO ---
    # O erro 'UnboundLocalError' acontece se o formulário for inválido.
    # Definimos o 'contexto' aqui no início para que ele sempre exista.
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
        # Preenche o formulário com o valor do plano do aluno como sugestão
        form = PagamentoForm(initial={'valor': aluno.plano.valor if aluno.plano else 0})

    # Adiciona o formulário (seja ele novo ou com erros) ao contexto
    contexto['form'] = form

    return render(request, 'gestao_academia/pagamento_form.html', contexto)

@login_required
def lista_pagamentos(request):
     # Começa com todos os pagamentos, ordenados pelos mais recentes
    queryset = Pagamento.objects.all().order_by('-data_pagamento')
     # --- LÓGICA DE PESQUISA E FILTRO ---
    termo_pesquisa = request.GET.get('pesquisa','')
    data_inicio =request.GET.get('data_inicio','')
    data_fim = request.GET.get('data_fim','') 

    if termo_pesquisa:
       # Filtra por nome do aluno que contenha o termo de pesquisa (icontains não diferencia maiúsculas/minúsculas)
       queryset = queryset.filter(aluno__nome_completo__icontains=termo_pesquisa)
    
    if data_inicio:
       # Filtra pagamentos feitos a partir da data de início (gte = greater than or equal)    
       queryset = queryset.filter(data_pagamento__gte=data_inicio)

    if data_fim:
        # Filtra pagamentos feitos até à data de fim (lte = less than or equal)
        queryset = queryset.filter(data_pagamento__lte=data_fim)

 # --- LÓGICA DE PAGINAÇÃO ---
    paginador = Paginator(queryset,10) # Mostra 10 pagamentos por página
    pagina_num = request.GET.get('pagina')
    pagina_obj = paginador.get_page(pagina_num)

    contexto = {
        # Em vez de 'pagamentos', enviamos o 'pagina_obj' que contém os itens da página atual
        'pagina_obj':pagina_obj,
        'titulo':'Histórico de Pagamentos',
        # Enviamos os termos de pesquisa de volta para os manter nos campos do formulário
        'termo_pesquisa': termo_pesquisa,
        'data_inicio' : data_inicio,
        'data_fim' : data_fim,

    }
    return render(request, 'gestao_academia/pagamento_lista.html', contexto)