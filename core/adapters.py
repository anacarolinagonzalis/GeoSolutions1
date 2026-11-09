from .mongo_utils import registrar_log_auditoria

class AuditLoggerAdapter:
    """
    Padrão Estrutural Adapter:
    Padroniza a interface de auditoria do sistema. Se amanhã o banco mudar
    do MongoDB para PostgreSQL ou serviços de log na nuvem, altera-se apenas
    este adaptador, sem modificar a Service Layer.
    """
    @staticmethod
    def log_evento(projeto_id, usuario, acao, detalhes=None):
        # Adapta a chamada interna para a função do MongoDB Atlas
        registrar_log_auditoria(
            projeto_id=projeto_id,
            usuario=usuario,
            acao=acao,
            detalhes=detalhes or {}
        )