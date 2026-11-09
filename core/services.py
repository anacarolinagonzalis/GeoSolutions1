from datetime import timedelta
from django.utils import timezone
from .models import Projeto, Cliente, ObservacaoCliente
from .mongo_utils import registrar_log_auditoria
from .viewmodels import ProjetoViewModel


def _obter_ou_criar_cliente(user):
    cliente = Cliente.objects.filter(usuario_vinculado=user).first()
    if not cliente:
        cnpj_temp = f"00000000{user.id:06d}"
        cliente = Cliente.objects.create(
            usuario_vinculado=user,
            nome_empresa=user.get_full_name() or user.username,
            cnpj=cnpj_temp,
            contato_nome=user.username,
            email=user.email or 'cliente@exemplo.com'
        )
    return cliente


class ProjetoService:
    @staticmethod
    def obter_projetos_do_cliente(user):
        """Retorna os projetos encapsulados na ViewModel para exibição formatada."""
        try:
            if user.is_staff:
                qs = Projeto.objects.all().order_by('-id')
            else:
                qs = Projeto.objects.filter(cliente__usuario_vinculado=user).order_by('-id')
            
            # Retorna a lista de objetos envelopados pela ViewModel
            return [ProjetoViewModel(p) for p in qs]
        except Exception:
            return []

    @staticmethod
    def contar_projetos_do_cliente(user):
        """Conta o número total de projetos do cliente."""
        if user.is_staff:
            return Projeto.objects.count()
        return Projeto.objects.filter(cliente__usuario_vinculado=user).count()

    @staticmethod
    def criar_solicitacao(user, titulo, tipo_servico=None, descricao=""):
        """
        Regra de Negócio (Service Layer):
        - Cria o projeto no SQL.
        - Salva o log de auditoria no NoSQL (MongoDB Atlas).
        - Grava observação se fornecida.
        """
        cliente = _obter_ou_criar_cliente(user)
        hoje = timezone.now().date()
        
        if tipo_servico:
            DIC_TIPOS_SERVICO = {
                'LICENCIAMENTO': 'Licenciamento Ambiental',
                'LAUDO_TECNICO': 'Laudo Técnico Ambiental',
                'ESTUDO_IMPACTO': 'EIA/RIMA',
                'OUTROS': 'Serviço Ambiental',
                'FALE_CONOSCO': 'FALE CONOSCO',
            }
            prefixo = DIC_TIPOS_SERVICO.get(tipo_servico, tipo_servico.replace('_', ' ').title())
            titulo_final = f"[{prefixo}] {titulo}"
        else:
            titulo_final = titulo

        # 1. SQL (SQLite)
        projeto = Projeto.objects.create(
            titulo=titulo_final,
            cliente=cliente,
            status='EM_ANALISE',
            data_inicio=hoje,
            prazo_vencimento=hoje + timedelta(days=30)
        )

        # 2. NoSQL (MongoDB Atlas)
        registrar_log_auditoria(
            projeto_id=projeto.id,
            usuario=user.username,
            acao="SOLICITACAO_PROJETO_CRIADA",
            detalhes={"titulo": projeto.titulo, "tipo_servico": tipo_servico or "DIRETO"}
        )

        # 3. Observação complementar
        if descricao:
            ObservacaoCliente.objects.create(
                projeto=projeto,
                autor=user,
                texto=descricao
            )

        return projeto


class ObservacaoService:
    @staticmethod
    def adicionar_observacao(projeto_id, user, texto):
        """Cria e salva uma nova observação vinculada ao projeto."""
        if not texto or not texto.strip():
            raise ValueError("O texto da observação não pode estar vazio.")
            
        projeto = Projeto.objects.get(id=projeto_id, cliente__usuario_vinculado=user)
        return ObservacaoCliente.objects.create(
            projeto=projeto,
            autor=user,
            texto=texto.strip()
        )