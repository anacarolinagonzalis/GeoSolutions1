# ADR 005 - Interface de Detalhamento de Projetos e Padronizacao de Templates

# Status
Aprovado

# Contexto
Após estruturar o painel básico, identificou-se a necessidade de permitir que os clientes visualizem informações detalhadas dos processos ambientais (status, prazos, órgãos envolvidos, documentos e tipo de serviço prestado via polimorfismo), além de poderem interagir enviando observações diretas para a equipe técnica.

# Problema
Como disponibilizar uma interface rica e intuitiva para o cliente, garantindo acessibilidade, usabilidade (IHC) e a correta localização dos arquivos de visualização pelo framework Django?

# Decisão
Criar o template `detalhe_projeto.html` com layout responsivo utilizando CSS nativo, estruturando o diretório de templates na convenção padrão do Django (`core/templates/core/`) e habilitando um formulário de envio de observações direto para o banco de dados.

# Justificativa
* A organização de arquivos no diretório `core/templates/core/` segue a convenção `app_directories` do Django, evitando erros de localização de templates (`TemplateDoesNotExist`).
* O design limpo e responsivo garante usabilidade e acessibilidade para clientes sem necessidade de frameworks pesados de frontend.
* A inclusão do formulário de observações atende ao requisito de comunicação direta com o cliente mantendo o histórico rastreável no sistema.

# Consequencias
* Todos os templates HTML do aplicativo `core` devem obrigatoriamente ser salvos dentro de `core/templates/core/`.
* A execução de comandos de gerenciamento do projeto no Ubuntu deve ser feira garantindo a utilização do ambiente Python 3 configurado (`python3 manage.py runserver`).

# Alternativa descartada
* **Uso de bibliotecas externas complexas de frontend (React/Vue):** Descartado para manter a simplicidade do projeto acadêmico e utilizar os recursos nativos do Django Templates.

# Commit
`feat: implementacao do template detalhe_projeto e padronizacao da estrutura de templates`