# gestao_academia/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Modalidade
from .forms import ModalidadeForm

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
