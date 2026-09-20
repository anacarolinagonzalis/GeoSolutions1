from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from .models import Perfil, Cliente, OrgaoAmbiental, Projeto, ServicoBase, ServicoLicenciamento, ServicoLaudoTecnico, DocumentoProjeto, ObservacaoCliente

class DocumentoInline(admin.TabularInline):
    model = DocumentoProjeto
    extra = 1

class ObservacaoInline(admin.TabularInline):
    model = ObservacaoCliente
    extra = 1

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'status', 'prazo_vencimento', 'responsavel')
    list_filter = ('status', 'orgao_ambiental', 'prazo_vencimento')
    search_fields = ('titulo', 'cliente__nome_empresa')
    inlines = [DocumentoInline, ObservacaoInline]

# Configuração do Polimorfismo no Admin
class ServicoLicenciamentoAdmin(PolymorphicChildModelAdmin):
    base_model = ServicoBase

class ServicoLaudoTecnicoAdmin(PolymorphicChildModelAdmin):
    base_model = ServicoBase

@admin.register(ServicoBase)
class ServicoBaseParentAdmin(PolymorphicParentModelAdmin):
    base_model = ServicoBase
    child_models = (ServicoLicenciamento, ServicoLaudoTecnico)

admin.site.register(Perfil)
admin.site.register(Cliente)
admin.site.register(OrgaoAmbiental)