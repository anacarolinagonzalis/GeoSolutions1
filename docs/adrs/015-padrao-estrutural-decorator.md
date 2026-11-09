# 15. Adição Dinâmica de Opcionais com o Padrão Decorator

# Status
Aprovado

## Contexto
No ecossistema da Moriah Geotecnologia, serviços ambientais podem receber serviços adicionais opcionais (como emissão urgente ou levantamento aéreo por drone). Alterar a estrutura do modelo principal de dados para cada novo adicional criaria rigidez e acoplamento desnecessário.

## Decisão
Implementar o padrão estrutural **Decorator** através da classe `ServicoDecorator` em `core/decorators.py`. Isso permite embrulhar dinamicamente o serviço ambiental base adicionando novos comportamentos, descrições e custos sem alterar a classe base.

## Consequências
* **Positivas:**
  - Princípio Open/Closed (Aberto para extensão, fechado para modificação).
  - Empilhamento flexível de opcionais e serviços adicionais.
  - Completa o Trio Estrutural da arquitetura (Adapter, Facade e Decorator).
* **Negativas:**
  - Pode gerar múltiplos pequenos objetos empilhados durante a execução.

## Observaçao
* Todo projeto desenvolvido com apoio de IA