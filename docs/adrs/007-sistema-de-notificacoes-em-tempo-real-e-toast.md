# 007. Sistema de Notificações em Tempo Real e Toast Flutuante

# *Status:
Aprovado

## Contexto
Quando um cliente cadastra uma nova demanda no portal, os administradores precisam ser notificados de imediato sem poluir a interface central da página inicial do admin.

## Decisão
1. Implementar um componente flutuante no canto inferior direito (*Toast Notification*).
2. Adicionar verificação assíncrona via `fetch` na rota `/admin/core/projeto/?status__exact=EM_ANALISE`.
3. Exibir o Toast e o ícone de sino (🔔) no menu superior **somente** se existirem projetos com o status `EM_ANALISE`.
4. Manter o centro da tela totalmente limpo e desimpedido para exibição do plano de fundo institucional.

## Consequências
* **Positivas:** Notificação discreta, responsiva e inteligente; o aviso só é visível quando realmente há pendências aguardando triagem.
* **Negativas:** Depende da requisição assíncrona (`fetch`) no carregamento do template base do admin.