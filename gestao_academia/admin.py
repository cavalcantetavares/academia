from django.contrib import admin
from .models import Modalidade #importa nosso modelo de modalidade
# Registra o modelo para que ele apareça na interface de admin
admin.site.register(Modalidade)