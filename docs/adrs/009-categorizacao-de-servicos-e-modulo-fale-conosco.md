# 009. Categorização de Serviços e Módulo Fale Conosco

# *Status:
Aprovado

## Contexto
Na tela de solicitação do cliente (`/cliente/solicitar/`), o formulário exigia a seleção prévia do tipo de serviço ambiental desejado, além de permitir o envio de dúvidas ou contatos gerais ("Fale Conosco") integrados ao mesmo fluxo.

## Decisão
1. Adicionar elemento `<select>` no template `solicitar_projeto.html` com os tipos de serviço: *Licenciamento Ambiental*, *Laudo Técnico*, *EIA/RIMA*, *Outros Serviços* e *Fale Conosco*.
2. Na `views.py`, utilizar um dicionário (`DIC_TIPOS_SERVICO`) para mapear as opções em títulos amigáveis e salvar observações iniciais em `ObservacaoCliente`.
3. Criar uma aba dedicada **💬 Fale Conosco** no menu do Admin direcionada para a busca filtrada `?q=FALE+CONOSCO`.
4. Corrigir o estado ativo das abas no JavaScript do `base_site.html` checando a query string (`search.includes('fale+conosco')`) para impedir que a aba "Projetos" e "Fale Conosco" fiquem selecionadas simultaneamente.

## Consequências
* **Positivas:** Facilita a triagem por parte da equipe técnica e separa dúvidas gerais de projetos em andamento no admin.
* **Negativas:** O filtro do Fale Conosco depende do prefixo `[FALE CONOSCO]` mantido na string do título do projeto.

## Observaçao
* Todo projeto desenvolvido com apoio de IA