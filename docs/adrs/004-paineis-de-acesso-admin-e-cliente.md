# ADR 004 - Separacao de Perfis de Acesso e Interface do Cliente

# Status
Aprovado

# Contexto
O sistema atenderá dois perfis distintos de usuários: a **Equipe Interna/Administrador** (que precisa gerenciar tudo) e os **Clientes** (que devem ter acesso estritamente limitado aos seus próprios processos).

# Problema
Como garantir usabilidade e segurança para que o cliente consulte apenas seus projetos e possa incluir observações sem comprometer o cadastro geral do sistema?

# Decisão
Utilizar a página nativa do **Django Admin** customizada para a gestão completa pela equipe técnica, e criar uma **Interface Web dedicada para o Cliente** com filtros de segurança por usuário (`request.user.cliente`).

# Justificativa
* O Django Admin já fornece uma interface completa e segura com filtros e busca para a equipe interna sem gastar tempo de desenvolvimento.
* A view customizada do cliente restringe a consulta via código, garantindo que a empresa X jamais visualize os projetos ou documentos da empresa Y.
* O cliente ganha um canal direto para enviar observações e acompanhar datas de vencimento em tempo real.

# Consequencias
* É necessário criar e manter o modelo `Perfil` para diferenciar o tipo de usuário no momento do login.
* O cadastro de novos projetos deve sempre estar vinculado ao usuário de um cliente específico.

# Alternativa descartada
* **Dar acesso ao Django Admin diretamente aos clientes:** Descartada por questões de segurança e poluição visual com recursos que o cliente não deve alterar.
* **Não ter área restrita para clientes:** Descartada pois deixaria o acompanhamento dependente de trocas manuais de e-mails e mensagens de WhatsApp.

# Commit
`feat: implementacao do painel restrito do cliente e personalizacao do admin`