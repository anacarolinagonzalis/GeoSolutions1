from .services import ProjetoService
from .adapters import AuditLoggerAdapter


class GeoSolutionsFacade:
    """
    Padrão Estrutural Facade:
    Fornece uma interface simplificada ("balcão único") para orquestrar
    a criação de projetos, registro de observações e auditoria no MongoDB Atlas.
    Esconde a complexidade de múltiplos subsistemas da camada de apresentação/views.
    """
    @staticmethod
    def criar_solicitacao_completa(user, titulo, tipo_servico=None, descricao=""):
        # 1. Delega a criação central para a Service Layer
        projeto = ProjetoService.criar_solicitacao(
            user=user,
            titulo=titulo,
            tipo_servico=tipo_servico,
            descricao=descricao
        )

        # 2. Garante o disparo da auditoria via Adapter
        AuditLoggerAdapter.log_evento(
            projeto_id=projeto.id,
            usuario=user.username,
            acao="SOLICITACAO_CRIADA_VIA_FACADE",
            detalhes={
                "titulo": projeto.titulo,
                "origem": "GeoSolutionsFacade"
            }
        )

        return projeto