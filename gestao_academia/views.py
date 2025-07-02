# gestao_academia/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Modalidade, Aluno, MatriculaModalidade, Plano, Faixa # Importações dos modelos
from .forms import ModalidadeForm, AlunoForm, MatriculaModalidadeForm # Importações dos formulários
from .models import Pagamento
from .forms import PagamentoForm
from django.core.paginator import Paginator
from .models import Instrutor, Turma
from .forms import InstrutorForm, TurmaForm
from datetime import date  # Importa a ferramenta de data
from .models import Aluno, Plano, Modalidade, Turma


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
    # --- NOVA LÓGICA PARA AS TURMAS DO DIA ---
    hoje = date.today()
    # O método isoweekday() retorna 1 para Segunda, 2 para Terça, etc.
    dia_semana_hoje = hoje.isoweekday()
    turmas_hoje = Turma.objects.filter(dia_da_semana=dia_semana_hoje).order_by('horario_inicio')

    contexto = {
        'total_alunos' : total_alunos,
        'total_planos' : total_planos,
        'total_modalidades' : total_modalidade,
        'ultimos_alunos' : ultimos_alunos,
        'turmas_hoje' : turmas_hoje,
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
            messages.success(request, 'Instrutor registrado com sucesso!')
            return redirect('lista_instrutores')  
    else:
        form = InstrutorForm()
        return render(request, 'gestao_academia/instrutor_form.html',{'form' : form, 'titulo':'Registrar novo Instrutor'}) 

@login_required
def instrutor_editar(request, pk):
    instrutor = get_object_or_404(Instrutor, pk=pk)
    if request.method == 'POST':
        form = InstrutorForm(request.POST, instance=instrutor)
        if form.is_valid():
            form.save()
            messages.success(request,'Dados do instrutor atualizados com sucesso')
            return redirect('lista_instrutores')
    else:
        form = InstrutorForm(instance=instrutor)
    return render(request, 'gestao_academia/instrutor_form.html',{'form':form, 'titulo':'Editar Instrutor'})

@login_required
def instrutor_apagar(request, pk):
    instrutor = get_object_or_404(Instrutor, pk=pk)
    if request.method == 'POST':
        instrutor.delete()
        messages.success(request, 'Instrutor removido com sucesso!')
        return redirect('lista_instrutores')
    return render(request, 'gestao_academia/instrutor_confirma_delete.html', {'instrutor': instrutor})    





# --- VIEWS PARA TURMAS/HORÁRIOS ---

@login_required
def grade_horarios(request):
    turmas = Turma.objects.all()
    # Organiza as turmas por dia da semana para exibir na grade
    dias_com_turmas = {}
    for dia_num, dia_nome in Turma.DIAS_SEMANA:
        turmas_do_dia = turmas.filter(dia_da_semana=dia_num)
        if turmas_do_dia:
            dias_com_turmas[dia_nome] = turmas_do_dia

    return render(request,'gestao_academia/grade_horarios.html', {'dias_com_turmas': dias_com_turmas})        



@login_required
def turma_criar(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma criada com sucesso')
        return redirect('grade_horarios')
    
    else:
        form = TurmaForm()
    return render(request, 'gestao_academia/turma_form.html', {'form': form, 'titulo': 'Criar Nova Turma'})    

# --- NOVAS VIEWS PARA EDITAR E APAGAR TURMA ---

@login_required
def turma_editar(request,pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
       form = TurmaForm(request.POST, instance=turma)
       if form.is_valid():
          form.save()
          messages.success(request,'Turma atualizada com secusso!')
          return redirect('grade_horarios')

    else:
        form = TurmaForm(instance=turma)
    return render(request, 'gestao_academia/turma_form.html', {'form': form, 'titulo': 'Editar Turma'}) 

@login_required
def turma_apagar(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        turma.delete()
        messages.success(request, 'Turma apagada com suscesso!')
        return redirect('grade_horarios')
    return render(request, 'gestao_academia/turma_confirm_delete.html',{'turma': turma})                
           
