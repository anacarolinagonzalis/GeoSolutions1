# 11. Extração da Regra de Negócio para Service Layer (SRP)

# Status
Aprovado

## Contexto
As *views* do Django acumulavam múltiplas responsabilidades (*Fat Views*): manipulação de requisições HTTP, regras ambientais da empresa, persistência SQL e envio de logs para o MongoDB Atlas, ferindo o Princípio da Responsabilidade Única (SRP).

## Decisão
Refatorar o sistema aplicando o padrão *Service Layer*. Toda a regra de negócio relacionada à criação e gestão de solicitações foi isolada nos métodos estáticos da classe `ProjetoService` em `core/services.py`, transformando as *views* do Django em *Thin Views*.

## Consequências
* **Positivas:**
  - *Views* magras e focadas apenas no ciclo de requisição/resposta HTTP.
  - Possibilidade de realizar testes automatizados da regra de negócio sem subir o servidor web.
  - Manutenibilidade centralizada das regras operacionais da Moriah Geotecnologia.
* **Negativas:**
  - Adição de uma camada extra de abstração no projeto.

## Observaçao
* Todo projeto desenvolvido com apoio de IA
