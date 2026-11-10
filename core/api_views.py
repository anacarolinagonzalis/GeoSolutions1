from rest_framework import viewsets
from .models import Projeto
from .serializers import ProjetoSerializer


class ProjetoViewSet(viewsets.ModelViewSet):
    """
    ViewSet que disponibiliza automaticamente as ações CRUD (GET, POST, PUT, DELETE)
    para o model Projeto.
    """
    queryset = Projeto.objects.all().order_by('-id')
    serializer_class = ProjetoSerializer