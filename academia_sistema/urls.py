# academia_sistema/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
# Importamos apenas as views necessárias
from gestao_academia import views as gestao_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. A página inicial ('') agora redireciona para a página de login.
    path('', RedirectView.as_view(url='/contas/login/', permanent=False), name='pagina_inicial'),

    # 2. O dashboard agora tem a sua própria URL. Adicionámos a barra no final.
    path('dashboard/', gestao_views.dashboard, name='dashboard'),

    # O resto das URLs continua igual
    path('contas/', include('contas.urls')),
    path('contas/', include('django.contrib.auth.urls')),
    path('gestao/', include('gestao_academia.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


