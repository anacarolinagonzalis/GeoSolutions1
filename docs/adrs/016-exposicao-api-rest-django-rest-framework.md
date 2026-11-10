# 16. Exposição de Recursos via API REST com Django REST Framework

# Status
Aprovado

## Contexto
O GeoSolutions precisava disponibilizar dados dos projetos ambientais para integração com sistemas externos, aplicativos móveis ou serviços de terceiros através de uma interface padronizada.

## Decisão
Adotar o **Django REST Framework (DRF)** para implementar os padrões de Serializer, ModelViewSet e Routers, expondo a rota `/api/projetos/` para operações CRUD com suporte a JSON e validações nativas.

## Consequências
* **Positivas:**
  - Padronização no formato JSON para integração com outros ecossistemas.
  - Interface navegável para testes e consumo de APIs.
  - Validações reutilizadas diretamente do modelo do Django.
* **Negativas:**
  - Adição de uma nova dependência de terceiros (`djangorestframework`).

  ## Observaçao
* Todo projeto desenvolvido com apoio de IA