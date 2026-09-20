from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Projeto, ObservacaoCliente

@login_required
def painel_cliente(request):
    # Restringe visualização apenas aos projetos pertencentes ao cliente logado
    try:
        cliente = request.user.cliente
        projetos = Projeto.objects.filter(cliente=cliente)
    except Exception:
        projetos = Projeto.objects.none()

    return render(request, 'core/painel_cliente.html', {'projetos': projetos})

@login_required
def detalhe_projeto_cliente(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk, cliente=request.user.cliente)
    
    if request.method == 'POST':
        texto_obs = request.POST.get('observacao')
        if texto_obs:
            ObservacaoCliente.objects.create(
                projeto=projeto,
                autor=request.user,
                texto=texto_obs
            )
            return redirect('detalhe_projeto_cliente', pk=pk)

    return render(request, 'core/detalhe_projeto.html', {'projeto': projeto})