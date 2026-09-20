# ADR 003 - Modelagem Relacional, Documental e Polimorfismo nos Servicos

# Status
Aprovado

# Contexto
A Moriah Geotecnologia presta diferentes tipos de serviços ambientais (como Licenciamento Ambiental e Laudos Técnicos). Cada serviço compartilha dados comuns (projeto, data de registro), mas possui informações específicas (número da licença, número da ART, área em hectares). Além disso, o sistema deve armazenar arquivos PDF de processos.

# Problema
Como estruturar o banco de dados para suportar diferentes tipos de serviços sem duplicar tabelas e como armazenar os documentos anexados de forma eficiente?

# Decisão
Utilizar o **Django ORM** com **Persistência Relacional** para o cadastro estruturado de entidades, a biblioteca `django-polymorphic` para **Polimorfismo** nos Serviços Ambientais, e a **Persistência Documental** para armazenamento de arquivos e pareceres anexados.

# Justificativa
* O Polimorfismo permite criar uma tabela pai (`ServicoBase`) e tabelas filhas específicas (`ServicoLicenciamento`, `ServicoLaudoTecnico`). Isso evita campos nulos no banco e não duplica código.
* A persistência de documentos via `FileField` vincula arquivos físicos de licenças e pareceres diretamente aos registros do banco relacional.

# Consequencias
* Necessidade de instalar e registrar o pacote `django-polymorphic`.
* As consultas de serviços no banco de dados trazem automaticamente a classe especializada correta.

# Alternativa descartada
* **Tabela Única com dezenas de campos nulos:** Descartada por poluir o banco de dados e gerar inconsistências quando um serviço não utiliza determinados campos.
* **Tabelas totalmente separadas sem relacionamento:** Descartada por dificultar a listagem unificada de todos os serviços de um projeto.

# Commit
`feat: criacao dos modelos de dados com suporte a polimorfismo e documentos`