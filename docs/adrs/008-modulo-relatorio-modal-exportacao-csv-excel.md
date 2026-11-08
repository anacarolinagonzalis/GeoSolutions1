# 008. Módulo de Relatórios e Exportação em Planilhas (CSV/Excel)

# *Status:
Aprovado

## Contexto
Necessidade de extração de relatórios e auditorias dos módulos cadastrados sem a necessidade de pacotes externos pesados de geração de PDF.

## Decisão
1. Adicionar o botão "Gerar Relatório" na barra de navegação superior do Admin.
2. Criar um modal interativo em CSS/JS permitindo a escolha do módulo (Clientes, Projetos, Laudos, Licenciamentos, etc.), período de datas e formato do arquivo (`.csv` ou `.xls`).
3. Processar os dados diretamente na tabela da listagem (`.results table`) ou gerar arquivo estruturado via Blob em JavaScript com codificação `UTF-8` (com BOM `\uFEFF` para correta acentuação no Microsoft Excel).

## Consequências
* **Positivas:** Exportação instantânea do lado do cliente (*client-side*), sem overhead no servidor Django.
* **Negativas:** A exportação direta da tabela DOM é limitada aos dados atualmente carregados/visíveis no *changelist*.