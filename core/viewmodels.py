from django.utils import timezone

class ProjetoViewModel:
    """
    Camada MVVM (ViewModel): Prepara e formata os dados do Projeto 
    exclusivamente para a exibição na interface (HTML/Templates),
    deixando a View limpa e testável sem desenhar tela.
    """
    STATUS_MAP = {
        'EM_ANALISE': {'rotulo': 'Em Análise', 'badge_class': 'bg-warning text-dark', 'icone': 'bi-hourglass-split'},
        'EM_ANDAMENTO': {'rotulo': 'Em Andamento', 'badge_class': 'bg-info text-white', 'icone': 'bi-gear-fill'},
        'CONCLUIDO': {'rotulo': 'Concluído', 'badge_class': 'bg-success text-white', 'icone': 'bi-check-circle-fill'},
        'CANCELADO': {'rotulo': 'Cancelado', 'badge_class': 'bg-danger text-white', 'icone': 'bi-x-circle-fill'},
    }

    def __init__(self, projeto):
        self.id = projeto.id
        self.titulo = projeto.titulo
        self.cliente_nome = projeto.cliente.nome_empresa if projeto.cliente else "N/A"
        self.status_codigo = projeto.status
        
        # Mapeamento visual
        status_info = self.STATUS_MAP.get(projeto.status, {
            'rotulo': projeto.get_status_display() if hasattr(projeto, 'get_status_display') else projeto.status,
            'badge_class': 'bg-secondary text-white',
            'icone': 'bi-info-circle'
        })
        
        self.status_rotulo = status_info['rotulo']
        self.badge_class = status_info['badge_class']
        self.icone = status_info['icone']

        # Formatação de datas para a tela
        self.data_inicio_fmt = projeto.data_inicio.strftime('%d/%m/%Y') if projeto.data_inicio else '-'
        self.prazo_vencimento_fmt = projeto.prazo_vencimento.strftime('%d/%m/%Y') if projeto.prazo_vencimento else '-'
        
        # Regra de exibição: Alerta de prazo vencido
        self.estavencido = False
        if projeto.prazo_vencimento and projeto.status not in ['CONCLUIDO', 'CANCELADO']:
            self.estavencido = projeto.prazo_vencimento < timezone.now().date()