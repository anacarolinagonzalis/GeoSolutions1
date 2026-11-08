from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from polymorphic.admin import (
    PolymorphicParentModelAdmin, 
    PolymorphicChildModelAdmin, 
    PolymorphicChildModelFilter
)


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

# --- REMOVER GRUPOS DO PAINEL DE ADMINISTRAÇÃO ---
if admin.site.is_registered(Group):
    admin.site.unregister(Group)

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
    show_in_index = True

class ServicoLaudoTecnicoAdmin(PolymorphicChildModelAdmin):
    base_model = ServicoBase
    show_in_index = True

@admin.register(ServicoLicenciamento)
class ServicoLicenciamentoDirectAdmin(ServicoLicenciamentoAdmin):
    pass

@admin.register(ServicoLaudoTecnico)
class ServicoLaudoTecnicoDirectAdmin(ServicoLaudoTecnicoAdmin):
    pass

@admin.register(ServicoBase)
class ServicoBaseParentAdmin(PolymorphicParentModelAdmin):
    base_model = ServicoBase
    child_models = (ServicoLicenciamento, ServicoLaudoTecnico)
    child_admin_classes = (ServicoLicenciamentoAdmin, ServicoLaudoTecnicoAdmin)
    list_display = ('nome_servico', 'projeto', 'data_registro')
    polymorphic_list_type_filter_title = "Tipo de Serviço"
    add_type_form_title = "Tipo de Serviço:"

# --- WIDGET PARA REMOVER O TEXTO TÉCNICO DE HASH E DEIXAR O BOTÃO VISÍVEL ---
class LimpoPasswordHashWidget(ReadOnlyPasswordHashWidget):
    def render(self, name, value, attrs=None, renderer=None):
        url = reverse('admin:auth_user_password_change', args=[self.instance.pk]) if hasattr(self, 'instance') and self.instance else '../password/'
        return format_html(
            '<a class="button" style="background-color: #f0f2f5 !important; color: #12341e !important; font-weight: 700; border: none; padding: 8px 16px; border-radius: 6px; text-decoration: none; box-shadow: 0 2px 4px rgba(0,0,0,0.15); display: inline-block;" href="{}">🔑 Alterar Senha do Usuário</a>', 
            url
        )

# --- FORMULÁRIO SIMPLIFICADO DE CRIAÇÃO DE USUÁRIO COM SELEÇÃO DE TIPO ---
class CustomUserCreationForm(UserCreationForm):
    TIPO_USUARIO_CHOICES = (
        ('cliente', 'Cliente (Acesso apenas à plataforma de clientes)'),
        ('gerente', 'Gerente / Sub-Administrador (Acesso de gestão ao Admin)'),
    )

    tipo_usuario = forms.ChoiceField(
        choices=TIPO_USUARIO_CHOICES,
        label="Nível de Acesso Inicial",
        widget=forms.RadioSelect,
        initial='cliente',
        help_text="Escolha 'Gerente' para liberar acesso ao Painel de Controle ou 'Cliente' para acesso externo."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        tipo = self.cleaned_data.get('tipo_usuario')
        if tipo == 'gerente':
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user

# --- CUSTOMIZAÇÃO DO USER ADMIN ---
if admin.site.is_registered(User):
    admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'tipo_usuario', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Nível de Acesso e Status da Conta', {
            'description': 'Configure abaixo o status do cadastro e os privilégios do usuário no sistema.',
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'is_active' in form.base_fields:
            form.base_fields['is_active'].label = "Conta Ativa no Sistema"
            form.base_fields['is_active'].help_text = "Se desmarcado, a conta é bloqueada temporariamente e o usuário não conseguirá fazer login no sistema."
        
        if 'is_staff' in form.base_fields:
            form.base_fields['is_staff'].label = "Gerente / Membro da Equipe (Acesso ao Painel Admin)"
            form.base_fields['is_staff'].help_text = "Marque esta opção para permitir que o usuário acesse o Painel Administrativo do GeoSolutions."
        
        if 'is_superuser' in form.base_fields:
            form.base_fields['is_superuser'].label = "Administrador Principal (Acesso Total)"
            form.base_fields['is_superuser'].help_text = "Concede controle total sobre o sistema, incluindo permissão exclusiva para excluir outros usuários."

        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        response = super().change_view(request, object_id, form_url, extra_context)
        if hasattr(self, 'form') and 'password' in self.form.base_fields:
            widget = LimpoPasswordHashWidget()
            widget.instance = self.get_object(request, object_id)
            self.form.base_fields['password'].widget = widget
            self.form.base_fields['password'].help_text = "As senhas são armazenadas de forma criptografada por segurança."
        return response

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        if obj and obj == request.user:
            return False
        return super().has_delete_permission(request, obj)

# --- OUTROS REGISTROS ---
admin.site.register(OrgaoAmbiental)

# --- CUSTOMIZAÇÃO DO TÍTULO DO PAINEL ---
admin.site.site_header = "GeoSolutions - Moriah Geotecnologia"
admin.site.site_title = "GeoSolutions Admin"
admin.site.index_title = "Painel de Controle e Gestão Ambiental"



# Adicione este bloco no final do seu core/admin.py:
class GlobalAdminStyle:
    class Media:
        css = {
            'all': ('core/css/custom_admin.css',)
        }

# Força o carregamento do CSS estático no Admin do Django
admin.site.__class__.Media = GlobalAdminStyle.Media