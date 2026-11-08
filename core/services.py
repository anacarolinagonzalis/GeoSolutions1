from .models import Projeto, ObservacaoCliente

class ProjetoService:
    @staticmethod
    def obter_projetos_do_cliente(user):
        """Retorna os projetos associados ao cliente do usuário logado."""
        try:
            cliente = user.cliente
            return Projeto.objects.filter(cliente=cliente)
        except Exception:
            return Projeto.objects.none()

    @staticmethod
    def contar_projetos_do_cliente(user):
        """Conta o número total de projetos do cliente."""
        return ProjetoService.obter_projetos_do_cliente(user).count()

class ObservacaoService:
    @staticmethod
    def adicionar_observacao(projeto_id, user, texto):
        """Cria e salva uma nova observação vinculada ao projeto."""
        if not texto or not texto.strip():
            raise ValueError("O texto da observação não pode estar vazio.")
            
        projeto = Projeto.objects.get(id=projeto_id, cliente=user.cliente)
        return ObservacaoCliente.objects.create(
            projeto=projeto,
            autor=user,
            texto=texto.strip()
        )