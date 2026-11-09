# 10. Persistência Híbrida (MongoDB Atlas) e Camada de Serviços (Service Layer)

# Status
Aprovado

## Contexto
O sistema GeoSolutions necessitava de uma solução para registar logs de auditoria flexíveis sem sobrecarregar a base de dados relacional (SQL). Adicionalmente, as *views* do Django acumulavam múltiplas responsabilidades (parsing HTTP, regras de negócio ambientais da empresa, persistência SQL e envio de logs NoSQL), ferindo o Princípio da Responsabilidade Única (SRP).

## Decisão
1. **Persistência Híbrida:** Adotar o **MongoDB Atlas (NoSQL)** em conjunto com o banco relacional (SQL). Os dados centrais permanecem no SQL, enquanto a coleção `logs_auditoria` no MongoDB Atlas recebe os eventos operacionais via `pymongo`.
2. **Camada de Serviços (Service Layer):** Extrair toda a regra de negócio e lógica de auditoria das views para a classe `ProjetoService` no ficheiro `core/services.py`, transformando as *views* do Django em *Thin Views*.

## Consequências
* **Positivas:**
  - Separação clara de responsabilidades (SRP) entre HTTP e Regra de Negócio.
  - *Views* mais magras e fáceis de manter (redução de código no `views.py`).
  - Isola os logs de auditoria num banco documental de alta flexibilidade.
  - Permite testes de unidade da regra de negócio sem a necessidade de simular requisições HTTP do Django.
* **Negativas:**
  - Adição de dependência externa (MongoDB Atlas e driver `pymongo`).
  - Criação de uma camada adicional de abstração no código (`services.py`).

## Observaçao
* Todo projeto desenvolvido com apoio de IA