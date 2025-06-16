#contas/urls.py
from django.urls import path
from . import views #Importa as views do app atual

urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    #Adcionaremos login, logout, etc., qui ou usaremos os do Django
]