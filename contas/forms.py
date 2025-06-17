# contas/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Define a regra de validação: ^[\w]+$ significa "começa e termina com um ou mais caracteres de palavra"
# Caracteres de palavra (\w) incluem letras (a-z, A-Z), números (0-9) e underscore (_).
username_validator = RegexValidator(
    r'^[\w]+$',
    'O nome de utilizador só pode conter letras, números e o caractere underscore (_).'
)

class CustomUserCreationForm(UserCreationForm):
    # Aqui estamos a substituir o campo de utilizador original.
    username = forms.CharField(
        label="Nome de utilizador",
        max_length=10,
        validators=[username_validator], # Aplicamos a nossa nova regra!
        help_text='Obrigatório. 10 caracteres ou menos. Apenas letras, números e _.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",) + UserCreationForm.Meta.fields[1:]