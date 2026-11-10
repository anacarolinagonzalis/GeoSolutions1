from rest_framework import serializers
from .models import Projeto


class ProjetoSerializer(serializers.ModelSerializer):
    """
    Serializer responsável por transformar a model Projeto em JSON
    e validar os dados de entrada no POST.
    """
    class Meta:
        model = Projeto
        fields = ['id', 'titulo', 'cliente', 'status', 'data_inicio', 'prazo_vencimento']