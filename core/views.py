from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Projeto
from .services import ProjetoService
from .viewmodels import ProjetoViewModel


@login_required
def painel_cliente(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo') or request.POST.get('nome')
        if titulo:
            ProjetoService.criar_solicitacao(user=request.user, titulo=titulo)
            return redirect('painel_cliente')

    projetos = ProjetoService.obter_projetos_do_cliente(request.user)
    total_projetos = ProjetoService.contar_projetos_do_cliente(request.user)

    context = {
        'projetos': projetos,
        'total_projetos': total_projetos,
    }
    
    return render(request, 'core/painel_cliente.html', context)


@login_required
def solicitar_projeto(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        tipo_servico = request.POST.get('tipo_servico')
        descricao = request.POST.get('descricao', '')

        if titulo and tipo_servico:
            ProjetoService.criar_solicitacao(
                user=request.user,
                titulo=titulo,
                tipo_servico=tipo_servico,
                descricao=descricao
            )
            return redirect('painel_cliente')

    return render(request, 'core/solicitar_projeto.html')


@login_required
def detalhe_projeto_cliente(request, pk):
    if request.user.is_staff:
        projeto_obj = get_object_or_404(Projeto, pk=pk)
    else:
        projeto_obj = get_object_or_404(Projeto, pk=pk, cliente__usuario_vinculado=request.user)

    # Encapsula o objeto no ViewModel para formatar os dados de exibição da tela
    projeto_vm = ProjetoViewModel(projeto_obj)
    return render(request, 'core/detalhe_projeto.html', {'projeto': projeto_vm})


@login_required
def contador_projetos_htmx(request):
    total = ProjetoService.contar_projetos_do_cliente(request.user)
    return render(request, 'core/_contador_projetos.html', {'total_projetos': total, 'total': total})