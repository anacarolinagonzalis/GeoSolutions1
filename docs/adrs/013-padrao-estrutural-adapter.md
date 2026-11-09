# 13. Isolamento da Infraestrutura com Padrão Adapter

# Status
Aprovado

## Contexto
O envio de logs de auditoria comunicava-se diretamente com o driver do MongoDB Atlas. Caso a infraestrutura de banco seja alterada ou seja necessário suportar múltiplos destinos de log, o código ficaria repleto de estruturas condicionais (`if/else`).

## Decisão
Implementar o padrão estrutural **Adapter** através da classe `AuditLoggerAdapter` em `core/adapters.py`, oferecendo uma interface genérica e estável para a camada de serviços.

## Consequências
* **Positivas:**
  - Desacoplamento entre a regra de negócio e os drivers de banco de dados.
  - Facilidade para trocar ou adicionar provedores de persistência de log.
* **Negativas:**
  - Introdução de uma camada simples de redirecionamento de chamadas.

## Observaçao
* Todo projeto desenvolvido com apoio de IA