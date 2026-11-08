from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from polymorphic.models import PolymorphicModel

# --- VALIDADOR PARA ACEITAR APENAS NÚMEROS ---
apenas_numeros = RegexValidator(
    regex=r'^\d+$',
    message='Este campo aceita apenas números.'
)

# --- PERFIS DE USUÁRIO ---
class Perfil(models.Model):
    TIPOS_USUARIO = (
        ('ADMIN', 'Administrador/Equipe'),
        ('CLIENTE', 'Cliente'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=10, choices=TIPOS_USUARIO, default='CLIENTE')
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_display()}"

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

# --- CADASTRO DE CLIENTE ---
class Cliente(models.Model):
    nome_empresa = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=20, unique=True)
    contato_nome = models.CharField(max_length=100)
    email = models.EmailField()
    usuario_vinculado = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    # CAMPOS DE TELEFONE COM VALORES PADRÃO
    ddi = models.CharField(
        max_length=3, 
        default="55", 
        blank=True,
        validators=[apenas_numeros], 
        verbose_name="Código do País (DDI)",
        help_text="Apenas números (Ex: 55)"
    )
    ddd = models.CharField(
        max_length=2, 
        default="11",
        blank=True,
        validators=[apenas_numeros], 
        verbose_name="Código de Área (DDD)",
        help_text="Apenas 2 dígitos (Ex: 11)"
    )
    telefone_numero = models.CharField(
        max_length=10, 
        default="000000000",
        blank=True,
        validators=[apenas_numeros], 
        verbose_name="Número do Telefone",
        help_text="Apenas números"
    )

    def __str__(self):
        return self.nome_empresa

    @property
    def telefone_completo(self):
        return f"+{self.ddi} ({self.ddd}) {self.telefone_numero}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

# --- ÓRGÃO AMBIENTAL ---
class OrgaoAmbiental(models.Model):
    nome = models.CharField(max_length=100)  # Ex: IBAMA, CETESB
    sigla = models.CharField(max_length=20)
    
    def __str__(self):
        return self.sigla

    class Meta:
        verbose_name = "Órgão Ambiental"
        verbose_name_plural = "Órgãos Ambientais"

# --- PROJETO AMBIENTAL ---
class Projeto(models.Model):
    STATUS_CHOICES = (
        ('EM_ANALISE', 'Em Análise'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('PENDENTE', 'Pendente com Órgão'),
        ('CONCLUIDO', 'Concluído'),
    )
    titulo = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='projetos')
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='projetos_responsaveis')
    orgao_ambiental = models.ForeignKey(OrgaoAmbiental, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EM_ANALISE')
    data_inicio = models.DateField(auto_now_add=True)
    prazo_vencimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.cliente.nome_empresa}"

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

# --- POLIMORFISMO EM SERVIÇOS AMBIENTAIS ---
class ServicoBase(PolymorphicModel):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='servicos')
    nome_servico = models.CharField(max_length=150)
    data_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome_servico

    class Meta:
        verbose_name = "Serviço Ambiental"
        verbose_name_plural = "Serviços Ambientais"

class ServicoLicenciamento(ServicoBase):
    numero_licenca = models.CharField(max_length=50)
    fase = models.CharField(max_length=50)  # LP, LI, LO

    class Meta:
        verbose_name = "Serviço de Licenciamento"
        verbose_name_plural = "Serviços de Licenciamento"

class ServicoLaudoTecnico(ServicoBase):
    area_estudo_hectares = models.DecimalField(decimal_places=2, max_digits=8)
    art_numero = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Laudo Técnico"
        verbose_name_plural = "Laudos Técnicos"

# --- PERSISTÊNCIA DOCUMENTAL E OBSERVAÇÕES DO CLIENTE ---
class DocumentoProjeto(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='documentos')
    titulo = models.CharField(max_length=100, blank=True, null=True)
    arquivo = models.FileField(upload_to='documentos_ambientais/', blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo or f"Documento #{self.id}"

    class Meta:
        verbose_name = "Documento do Projeto"
        verbose_name_plural = "Documentos dos Projetos"

class ObservacaoCliente(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='observacoes')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Observação de {self.autor.username} em {self.projeto.titulo}"

    class Meta:
        verbose_name = "Observação do Cliente"
        verbose_name_plural = "Observações dos Clientes"

# Tradução dos nomes nativos do Django no Admin
Group._meta.verbose_name = "Grupo"
Group._meta.verbose_name_plural = "Grupos"
User._meta.verbose_name = "Usuário"
User._meta.verbose_name_plural = "Usuários"