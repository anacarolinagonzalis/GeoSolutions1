# 12. Separação da Lógica de Apresentação com MVVM (ViewModel)

# Status
Aprovado


## Contexto
Após a extração da regra de negócio para a Service Layer, a lógica de formatação visual (cores de badges, textos de status, ícones e formatação de datas) ainda poluía as views e templates.

## Decisão
Adotar o padrão **MVVM (Model-View-ViewModel)** criando a classe `ProjetoViewModel` em `core/viewmodels.py`. Os objetos de modelo são envelopados para preparar os dados de exibição antes de serem enviados à camada de apresentação.

## Consequências
* **Positivas:**
  - Lógica de exibição testável em Python sem desenhar tela HTML.
  - Templates mais limpos e declarativos.
* **Negativas:**
  - Pequeno aumento no consumo de memória ao criar instâncias de wrapper para listas de objetos.

## Observaçao
* Todo projeto desenvolvido com apoio de IA
