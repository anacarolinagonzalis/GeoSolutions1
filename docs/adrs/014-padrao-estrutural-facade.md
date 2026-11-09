# 14. Orquestração de Subsistemas com o Padrão Facade

# Status
Aprovado

## Contexto
A criação de uma solicitação no GeoSolutions envolve a coordenação de múltiplos subsistemas: persistência relacional (SQL), criação de registros de observação e log de auditoria no NoSQL (MongoDB Atlas).

## Decisão
Implementar o padrão estrutural **Facade** através da classe `GeoSolutionsFacade` no ficheiro `core/facades.py`. A camada de visualização interage com uma única interface unificada que oculta a complexidade de orquestração das operações.

## Consequências
* **Positivas:**
  - Ponto de entrada único para operações complexas que envolvem múltiplos subsistemas.
  - Redução do acoplamento entre a camada HTTP/Views e os subsistemas internos.
  - Diferenciação clara entre Adapter (adaptação de interface única) e Facade (orquestração de múltiplos subsistemas).
* **Negativas:**
  - A classe Facade pode tornar-se um ponto centralizador caso receba responsabilidades em excesso.

## Observaçao
* Todo projeto desenvolvido com apoio de IA