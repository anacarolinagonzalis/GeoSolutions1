from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
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


@login_required
@user_passes_test(lambda u: u.is_staff)
def relatorio_projetos(request):
    # Pega os IDs dos projetos selecionados no Admin
    ids_selecionados = request.GET.get('ids', '').split(',')
    
    if ids_selecionados and ids_selecionados[0]:
        projetos = Projeto.objects.filter(id__in=ids_selecionados)
    else:
        projetos = Projeto.objects.all()

    return render(request, 'core/relatorio_projetos.html', {'projetos': projetos})