from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages # Para exibir mensagens ao usuario


def resgistrar ( request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid();
        form.save() # Salva o novo usuario no banco de dados
        username = form.cleaned_data.get('username')