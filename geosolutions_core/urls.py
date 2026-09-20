from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cliente/painel/', views.painel_cliente, name='painel_cliente'),
    path('cliente/projeto/<int:pk>/', views.detalhe_projeto_cliente, name='detalhe_projeto_cliente'),
]