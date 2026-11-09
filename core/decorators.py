from abc import ABC, abstractmethod


class ServicoAmbientalComponent(ABC):
    """Componente Base para os Serviços Ambientais (Interface)"""
    @abstractmethod
    def get_descricao(self) -> str:
        pass

    @abstractmethod
    def get_custo_adicional(self) -> float:
        pass


class ServicoBase(ServicoAmbientalComponent):
    """Serviço Ambiental Padrão"""
    def __init__(self, nome_servico: str):
        self.nome_servico = nome_servico

    def get_descricao(self) -> str:
        return self.nome_servico

    def get_custo_adicional(self) -> float:
        return 0.0


class ServicoDecorator(ServicoAmbientalComponent):
    """Decorator Base"""
    def __init__(self, servico: ServicoAmbientalComponent):
        self._servico = servico

    def get_descricao(self) -> str:
        return self._servico.get_descricao()

    def get_custo_adicional(self) -> float:
        return self._servico.get_custo_adicional()


class TaxaUrgenciaDecorator(ServicoDecorator):
    """Acrescenta taxa de atendimento prioritário ao serviço"""
    def get_descricao(self) -> str:
        return f"{self._servico.get_descricao()} + [Urgência/Prioritário]"

    def get_custo_adicional(self) -> float:
        return self._servico.get_custo_adicional() + 500.0


class RelatorioDroneDecorator(ServicoDecorator):
    """Acrescenta mapeamento aéreo fotográfico via drone ao serviço"""
    def get_descricao(self) -> str:
        return f"{self._servico.get_descricao()} + [Levantamento com Drone]"

    def get_custo_adicional(self) -> float:
        return self._servico.get_custo_adicional() + 1200.0