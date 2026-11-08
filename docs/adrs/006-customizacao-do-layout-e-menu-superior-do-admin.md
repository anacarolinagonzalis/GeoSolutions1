# 006. Customização do Layout e Menu Superior do Admin

# *Status: 
Aprovado

## Contexto
O Django Admin nativo possui uma barra lateral (sidebar) padrão e visual genérico. Para a plataforma GeoSolutions, era necessário alinhar o painel às cores institucionais da Moriah Geotecnologia (`#12341e` e `#e2f0d9`), remover elementos sem uso (como navegação lateral) e disponibilizar um menu horizontal superior para navegação rápida entre os módulos de gestão.

## Decisão
1. Sobrescrever o template `admin/base_site.html`.
2. Ocultar a sidebar padrão (`#nav-sidebar`) via CSS e definir o background customizado com marca d'água (`logo_fundo.png`).
3. Injetar via JavaScript uma barra de navegação horizontal superior (`.top-nav-bar`) no cabeçalho com links para todos os módulos (Clientes, Projetos, Laudos, Licenciamentos, Serviços e Órgãos).
4. Implementar rotinas em JavaScript para indicar a aba ativa com base na URL acessada.

## Consequências
* **Positivas:** Interface moderna, corporativa, mais limpa para os administradores e perfeitamente integrada à identidade visual da empresa.
* **Negativas:** Requer manutenção manual do array de links no template caso novos módulos sejam adicionados ao admin no futuro.