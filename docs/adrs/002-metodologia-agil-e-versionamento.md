# ADR 002 - Adocao do Scrum no Taiga e Versionamento com Git/GitHub

# Status
Aprovado

# Contexto
O projeto precisa ser desenvolvido em 4 Sprints, com tarefas divididas entre a equipe de estudantes, garantindo rastreabilidade do código e entregas contínuas.

# Problema
Como gerenciar o fluxo de trabalho da equipe, organizar o backlog das 4 Sprints e garantir que o código-fonte esteja seguro, versionado e sincronizado no GitHub?

# Decisão
Adotar a metodologia ágil **Scrum** utilizando a ferramenta **Taiga** para a gestão de tarefas e o **Git/GitHub** com script de automação no Ubuntu para versionamento de código.

# Justificativa
* O Taiga oferece suporte nativo e gratuito ao framework Scrum (Backlog, User Stories, Sprints e quadro Kanban).
* O Git/GitHub permite que toda a equipe trabalhe no mesmo código e guarde o histórico de alterações.
* A criação de um script `.sh` automatiza o envio de commits no terminal do Ubuntu, evitando erros de digitação de comandos.

# Consequencias
* Todos os membros da equipe devem atualizar o status das tarefas diariamente no Taiga.
* É necessário rodar o script de sincronização sempre que uma nova funcionalidade for finalizada.

# Alternativa descartada
* **Trello:** Descartado por não ter suporte nativo ao Scrum (sprints, pontos de história) de forma direta na versão gratuita.
* **Envio manual de arquivos por e-mail/ZIP:** Descartado por ser propenso a perda de código e falta de controle de versões.

# Commit
`docs: criacao do script de automacao do git e integracao com github`