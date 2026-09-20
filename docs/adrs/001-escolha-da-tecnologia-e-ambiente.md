# ADR 001 - Escolha do Ambiente de Desenvolvimento e Framework Web

# Status
Aprovado

# Contexto
A empresa Moriah Geotecnologia necessita de um sistema de Gestão Ambiental para centralizar o acompanhamento de projetos, prazos e clientes. A equipe de desenvolvimento é composta por estudantes iniciantes que utilizam o sistema operacional Ubuntu via virtualizador.

# Problema
Qual ambiente de desenvolvimento, linguagem e framework devemos utilizar para construir um protótipo web funcional, seguro e de rápido desenvolvimento, que suporte banco de dados relacional e controle de permissões?

# Decisão
Decidimos utilizar a linguagem **Python** na versão 3 com o framework **Django**, executados dentro de um ambiente virtual (`.venv`) no sistema operacional **Ubuntu**.

# Justificativa
* O Python é uma linguagem simples de aprender e amplamente utilizada no mercado.
* O Django já vem com uma estrutura pronta contendo painel administrativo, autenticação de usuários, segurança e ORM (banco de dados) sem a necessidade de instalar bibliotecas extras complexas.
* O uso do `.venv` garante que as dependências do projeto não interfiram no sistema operacional.

# Consequencias
* A equipe precisará aprender a estrutura padrão do Django (Model, View, Template).
* O projeto fica dependente da estrutura de diretórios do Django.
* A curva de aprendizado inicial é reduzida por conta das ferramentas nativas do framework.

# Alternativa descartada
* **Node.js com Express:** Descartado por exigir a configuração manual de banco de dados, rotas e painel administrativo, o que aumentaria a complexidade para desenvolvedores iniciantes.
* **PHP Nativo:** Descartado devido ao maior risco de falhas de segurança e falta de padronização na estrutura do projeto.

# Commit
`init: criacao do ambiente python venv e estrutura base django`