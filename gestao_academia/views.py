# gestao_academia/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Modalidade
from .forms import ModalidadeForm
from .models import Modalidade, Aluno # Adicione Aluno 
from .forms import ModalidadeForm, AlunoForm # Adicione AlunoForm

# View para listar (já existente)
def lista_modalidades(request):
    modalidades = Modalidade.objects.all()
    return render(request, 'gestao_academia/lista_modalidades.html', {'modalidades': modalidades})

# View para CRIAR uma nova modalidade
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

# View para EDITAR uma modalidade existente
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

# View para APAGAR uma modalidade existente
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
    return render(request, 'gestao_academia/aluno_lista.html', {'aluno': alunos })

@login_required
def aluno_detalhe(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'gestao_academia/aluno_detalhe.html', {'aluno' : aluno})

@login_required
def aluno_criar(request):
    if request.method == 'POST':
        # request.FILES é necessário para lidar com o upload de ficheiros (a foto)
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno registrado com sucesso!')
            return redirect('lista_alunos')
    else:
        form = AlunoForm()
    return render(request, 'gestao_academia/aluno_form.html',{'form': form, 'titulo': 'Registrar Novo Aluno'})
    
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
    if request.method == 'POST' :
        aluno.delete()
        messages.success(request, 'Aluno apagado com sucesso!')
        return redirect('lista_alunos')
    return render(request, 'gestao_academia/aluno_confirm_delete.html',{'aluno': aluno})   
