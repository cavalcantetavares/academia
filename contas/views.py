from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages # Para exibir mensagens ao usuario


def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}! Você já pode fazer login.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'contas/registrar.html', {'form': form})

def pagina_inicial(request):
    return render(request, 'pagina_inicial.html')
