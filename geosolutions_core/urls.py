from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from core import views
from core.api_views import ProjetoViewSet

# Configuração do Router do Django REST Framework
router = DefaultRouter()
router.register(r'projetos', ProjetoViewSet, basename='projeto-api')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rotas de Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='core/cliente_login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Rotas da Aplicação do Cliente
    path('', views.painel_cliente, name='home'),
    path('cliente/painel/', views.painel_cliente, name='painel_cliente'),
    path('cliente/solicitar/', views.solicitar_projeto, name='solicitar_projeto'),
    path('cliente/projeto/<int:pk>/', views.detalhe_projeto_cliente, name='detalhe_projeto_cliente'),
    path('cliente/contador-htmx/', views.contador_projetos_htmx, name='contador_projetos_htmx'),

    # Rota da API REST Navegável
    path('api/', include(router.urls)),
]