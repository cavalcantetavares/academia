"""
URL configuration for academia_sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from contas import views as contas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', contas_views.pagina_inicial, name='pagina_inicial'),
    path('contas/', include('contas.urls')),
    path('contas/', include('django.contrib.auth.urls')),

    # --- CORREÇÃO FINAL ---
    # A única linha para o nosso novo app deve ser esta.
    # Ela diz ao Django para procurar as URLs de gestão no outro ficheiro.
    path('gestao/', include('gestao_academia.urls')),
]


