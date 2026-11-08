from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Projeto, Cliente, ObservacaoCliente


def _obter_ou_criar_cliente(user):
    cliente = Cliente.objects.filter(usuario_vinculado=user).first()
    if not cliente:
        cnpj_temp = f"00000000{user.id:06d}"
        cliente = Cliente.objects.create(
            usuario_vinculado=user,
            nome_empresa=user.get_full_name() or user.username,
            cnpj=cnpj_temp,
            contato_nome=user.username,
            email=user.email or 'cliente@exemplo.com'
        )
    return cliente


@login_required
def painel_cliente(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo') or request.POST.get('nome')
        
        if titulo:
            cliente = _obter_ou_criar_cliente(request.user)
            hoje = timezone.now().date()
            
            Projeto.objects.create(
                titulo=titulo,
                cliente=cliente,
                status='EM_ANALISE',
                data_inicio=hoje,
                prazo_vencimento=hoje + timedelta(days=30)
            )
            return redirect('painel_cliente')

    if request.user.is_staff:
        projetos = Projeto.objects.all().order_by('-id')
    else:
        projetos = Projeto.objects.filter(cliente__usuario_vinculado=request.user).order_by('-id')

    total_projetos = projetos.count()

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
            cliente = _obter_ou_criar_cliente(request.user)
            hoje = timezone.now().date()
            
            # Mapeamento para rótulos legíveis no título do projeto
            DIC_TIPOS_SERVICO = {
                'LICENCIAMENTO': 'Licenciamento Ambiental',
                'LAUDO_TECNICO': 'Laudo Técnico Ambiental',
                'ESTUDO_IMPACTO': 'EIA/RIMA',
                'OUTROS': 'Serviço Ambiental',
                'FALE_CONOSCO': 'FALE CONOSCO',
            }

            prefixo = DIC_TIPOS_SERVICO.get(tipo_servico, tipo_servico.replace('_', ' ').title())
            titulo_final = f"[{prefixo}] {titulo}"

            projeto = Projeto.objects.create(
                titulo=titulo_final,
                cliente=cliente,
                status='EM_ANALISE',
                data_inicio=hoje,
                prazo_vencimento=hoje + timedelta(days=30)
            )

            # Grava a descrição enviada no modelo ObservacaoCliente
            if descricao:
                ObservacaoCliente.objects.create(
                    projeto=projeto,
                    autor=request.user,
                    texto=descricao
                )

            return redirect('painel_cliente')

    return render(request, 'core/solicitar_projeto.html')


@login_required
def detalhe_projeto_cliente(request, pk):
    if request.user.is_staff:
        projeto = get_object_or_404(Projeto, pk=pk)
    else:
        projeto = get_object_or_404(Projeto, pk=pk, cliente__usuario_vinculado=request.user)

    return render(request, 'core/detalhe_projeto.html', {'projeto': projeto})


@login_required
def contador_projetos_htmx(request):
    if request.user.is_staff:
        total = Projeto.objects.count()
    else:
        total = Projeto.objects.filter(cliente__usuario_vinculado=request.user).count()
        
    return render(request, 'core/_contador_projetos.html', {'total': total})