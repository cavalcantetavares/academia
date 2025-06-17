# gestao_academia/urls.py
from django.contrib import admin
from django.urls import path, include
from contas import views as contas_wiews
from django.urls import path
from . import views # Importa as views deste app (gestao_academia)


urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('contas/', include('contas.urls')),
    #path('contas/', include('django.contrib.auth.urls')),
    # ADICIONE ESTA LINHA:
    # Qualquer URL que comece com 'gestao/' será procurada no ficheiro urls.py de gestao_academia
    #path('gestao/', include('gestao_academia.urls')),
    #path('modalidades/', views.lista_modalidades, name='lista_modalidades'),
    path('modalidades/', views.lista_modalidades, name='lista_modalidades'),
    path('modalidades/nova/', views.criar_modalidade, name='criar_modalidade'),
    path('modalidades/<int:pk>/editar/', views.editar_modalidade, name='editar_modalidade'),
    path('modalidades/<int:pk>/apagar/', views.apagar_modalidade, name='apagar_modalidade'),
    
]
