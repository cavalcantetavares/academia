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
from django.urls import path, include #adicione 'include' para incluir urls de outros apps
from contas import views as contas_views # para a pagina inicial

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', contas_views.pagina_inicial,name = 'pagina_inicial'), # Nossa página inicial
    path('contas/', include('contas.urls')), # Inclui as URLs do app 'contas'
    path('contas/', include('django.contrib.auth.urls')),# Inclui URLs prontas do Django para login, logout, reset de senha, etc.                                                       # Isso fornece rotas como /contas/login/, /contas/logout/
]


