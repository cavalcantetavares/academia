# academia_sistema/urls.py

from django.contrib import admin
from django.urls import path, include
from gestao_academia import views as gestao_views 
from contas import views as contas_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URLs do Admin e da Página Inicial
    path('admin/', admin.site.urls),
     # A NOSSA NOVA PÁGINA INICIAL É O DASHBOARD
    path('', gestao_views.dashboard, name='dashboard'),

    # Inclui as URLs do app de Contas
    path('contas/', include('contas.urls')),
    path('contas/', include('django.contrib.auth.urls')),

    # Inclui as URLs do app de Gestão
    path('gestao/', include('gestao_academia.urls')),
]

# Configuração para servir ficheiros de média em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


