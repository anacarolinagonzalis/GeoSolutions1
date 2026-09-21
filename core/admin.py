from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from .models import (
    Perfil, 
    Cliente, 
    OrgaoAmbiental, 
    Projeto, 
    ServicoBase, 
    ServicoLicenciamento, 
    ServicoLaudoTecnico, 
    DocumentoProjeto, 
    ObservacaoCliente
)
from .forms import ClienteForm

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

# --- ADMIN DE CLIENTES COM FORMULÁRIO DE MÁSCARA ---
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm
    list_display = ('nome_empresa', 'cnpj', 'contato_nome', 'email', 'telefone_completo')
    search_fields = ('nome_empresa', 'cnpj', 'contato_nome')

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

# --- WIDGET PARA MANTER O BOTÃO E REMOVER O TEXTO TÉCNICO DO HASH ---
class LimpoPasswordHashWidget(ReadOnlyPasswordHashWidget):
    def render(self, name, value, attrs=None, renderer=None):
        url = reverse('admin:auth_user_password_change', args=[self.instance.pk]) if hasattr(self, 'instance') and self.instance else '../password/'
        return format_html('<a class="button" href="{}">Reconfigurar senha</a>', url)

# --- REMOVER HASH DA SENHA E CUSTOMIZAR USER ADMIN ---
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        widget = LimpoPasswordHashWidget()
        widget.instance = self.get_object(request, object_id)
        self.form.base_fields['password'].widget = widget
        self.form.base_fields['password'].help_text = "As senhas são armazenadas de forma criptografada por segurança."
        return super().change_view(request, object_id, form_url, extra_context)

# --- OUTROS REGISTROS ---
admin.site.register(Perfil)
admin.site.register(OrgaoAmbiental)

# --- CUSTOMIZAÇÃO DO TÍTULO DO PAINEL ---
admin.site.site_header = "GeoSolutions - Moriah Geotecnologia"
admin.site.site_title = "GeoSolutions Admin"
admin.site.index_title = "Painel de Controle e Gestão Ambiental"