from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from .models import Perfil, Cliente, OrgaoAmbiental, Projeto, ServicoBase, ServicoLicenciamento, ServicoLaudoTecnico, DocumentoProjeto, ObservacaoCliente

# --- INLINES ---
class DocumentoInline(admin.TabularInline):
    model = DocumentoProjeto
    extra = 1

class ObservacaoInline(admin.TabularInline):
    model = ObservacaoCliente
    extra = 1

# --- AÇÃO EM LOTE PARA GERAR RELATÓRIO ---
@admin.action(description="📄 Gerar Relatório Selecionados (Impressão/PDF)")
def gerar_relatorio_action(modeladmin, request, queryset):
    selected_ids = ",".join(str(obj.id) for obj in queryset)
    url = reverse('relatorio_projetos') + f"?ids={selected_ids}"
    return HttpResponseRedirect(url)

# --- ADMIN DE PROJETOS ---
@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'status', 'prazo_vencimento', 'responsavel')
    list_filter = ('status', 'orgao_ambiental', 'prazo_vencimento')
    search_fields = ('titulo', 'cliente__nome_empresa')
    actions = [gerar_relatorio_action]
    inlines = [DocumentoInline, ObservacaoInline]

# --- ADMIN DE SERVIÇOS POLIMÓRFICOS ---
class ServicoLicenciamentoAdmin(PolymorphicChildModelAdmin):
    base_model = ServicoBase

class ServicoLaudoTecnicoAdmin(PolymorphicChildModelAdmin):
    base_model = ServicoBase

@admin.register(ServicoBase)
class ServicoBaseParentAdmin(PolymorphicParentModelAdmin):
    base_model = ServicoBase
    child_models = (ServicoLicenciamento, ServicoLaudoTecnico)

# --- OUTROS REGISTROS ---
admin.site.register(Perfil)
admin.site.register(Cliente)
admin.site.register(OrgaoAmbiental)

# --- CUSTOMIZAÇÃO DO TÍTULO DO PAINEL ---
admin.site.site_header = "GeoSolutions - Moriah Geotecnologia"
admin.site.site_title = "GeoSolutions Admin"
admin.site.index_title = "Painel de Controle e Gestão Ambiental"