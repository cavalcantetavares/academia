
from django.shortcuts import render, redirect
# REMOVA a importação antiga do UserCreationForm
# from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from .forms import CustomUserCreationForm # <--- IMPORTE O SEU NOVO FORMULÁRIO

def registrar(request):
    if request.method == 'POST':
        # Use o seu formulário personalizado aqui
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}! Você já pode fazer login.')
            return redirect('login')
    else:
        # E aqui também
        form = CustomUserCreationForm() 

    return render(request, 'contas/registrar.html', {'form': form})

# A view pagina_inicial continua igual
#def pagina_inicial(request):
#    return render(request, 'pagina_inicial.html')