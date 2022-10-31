from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib import messages

from SistemaDeSolicitacoes.models import MensagemAudiovisual, MensagemDisciplina, MensagemCurso, SolicitacaoAudiovisual, SolicitacaoCurso, SolicitacaoDisciplina
from SistemaDeSolicitacoes.forms import SolicitacaoAudiovisualForm, SolicitacaoAvaliacaoForm, SolicitacaoCursoForm, SolicitacaoDisciplinaForm

from braces.views import GroupRequiredMixin

from SistemaDeSolicitacoes.utils import SendEmail

EMAIL_BODIES = {
    # AUDIOVISUAL
    "nova_solicitacao_audiovisual": {
        "subject": "CEAD UFJF | Solicitação de Serviço Audiovisual",
        "message": "Há uma nova solicitação de serviço Audiovisual em sua caixa de entrada."
    },
    "formulario_audiovisual_deferido": {
        "subject": "CEAD UFJF | Solicitação de Serviço de Audiovisual",
        "message": "Solicitação de serviço de audiovisual aprovada pela coordenação do CEAD."
    },
    "formulario_audiovisual_indeferido": {
        "subject": "CEAD UFJF | Análise da Solicitação de Serviço Audiovisual",
        "message": "Olá! Sua solicitação de serviço audiovisual necessita de alguns ajustes."
    },

    # CURSO
    "nova_solicitacao_de_curso": {
        "subject": "CEAD UFJF | Solicitacao de Curso",
        "message": "Há uma nova solicitação de curso em sua caixa de entrada."
    },
    "formulario_curso_deferido": {
        "subject": "CEAD UFJF | Análise da Solicitação de Abertura de Curso",
        "message": "Solicitação de abertura de curso aprovada pelo setor acadêmico"
    },
    "formulario_curso_indeferido": {
        "subject": "CEAD UFJF | Análise da Solicitação de Abertura de Curso",
        "message": "Olá! Sua solicitação de abertura de curso necessita de alguns ajustes."
    },

    # DISCIPLINA
    "nova_solicitacao_de_disciplina": {
        "subject": "CEAD UFJF | Solicitação de Disciplina",
        "message": "Há uma nova solicitação de disciplina em sua caixa de entrada."
    },
    "formulario_disciplina_deferido": {
        "subject": "CEAD UFJF | Análise da Solicitação de Abertura de Disciplina",
        "message": "Solicitação de abertura de disciplina aprovada pelo setor acadêmico"
    },
    "formulario_disciplina_indeferido": {
        "subject": "CEAD UFJF | Análise da Solicitação de Abertura de Disciplina",
        "message": "Olá! Sua solicitação de abertura de disciplina necessita de alguns ajustes."
    },
}

# Create your views here.
def Index(request):
    if request.user.is_anonymous:
        return redirect('login')
    context = {'groups': []}
    if 'Suporte' in [group.name for group in request.user.groups.all()]:
        context['groups'].append('Suporte')
    elif 'Acadêmico' in [group.name for group in request.user.groups.all()]:
        context['groups'].append('Acadêmico')
    elif 'Produção' in [group.name for group in request.user.groups.all()]:
        context['groups'].append('Produção')
    else:
        context = {}
    return render(request, 'SistemaDeSolicitacoes/index.html', context)

class SolicitacaoDisciplinaCreateView(CreateView):
    form_class = SolicitacaoDisciplinaForm
    template_name = 'SistemaDeSolicitacoes/solicitacao_de_disciplina.html'
    success_url = 'index'

    def form_valid(self, form):
        solicitacao = form.save(commit=False)
        solicitacao.status = 'A'
        solicitacao.grupos = form.cleaned_data['grupos']
        solicitacao.conteudo_passado = form.cleaned_data['conteudo_passado']
        solicitacao.save()
        messages.success(self.request, 'Solicitação criada com sucesso!')
        #DISPARAR EMAIL PARA O ACADÊMICO
        new_email = SendEmail(
            subject="Nova Solicitação de Abertura de Disciplina | CEAD/UFJF",
            recipients=["academico.cead@ufjf.br"],
            message="""
                Uma nova solicitação de abertura de disciplina foi aberta por {}:

                E-mail do Responsável: {},
                Disciplina: {},
                Curso: {},
                Início das atividades: {}

                Para mais detalhes, favor acessar o Sistema de Solicitações.


                Att.,
                CEAD/UFJF
            """.format(
                form.cleaned_data['professor_responsavel'], 
                form.cleaned_data['email'],
                form.cleaned_data['nome_disciplina'], 
                form.cleaned_data['curso_disciplina'],
                form.cleaned_data['atividades_inicio'].strftime('%d/%m/%Y')
            )
        )
        # new_email.send()
        return redirect('index')

class SolicitacaoDisciplinaEntradaAcademicoListView(ListView, GroupRequiredMixin):
    model = SolicitacaoDisciplina
    template_name = 'SistemaDeSolicitacoes/disciplina_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = u'Acadêmico'

    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='A').filter(professor_responsavel__icontains=search) | queryset.filter(status='A').filter(nome_disciplina__icontains=search) 
        else:
            return queryset.filter(status='A')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoDisciplinaEntradaAcademicoListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoDisciplina.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoDisciplina.objects.filter(status='E')
        context['pendentes'] = SolicitacaoDisciplina.objects.filter(status='P')
        context['fechadas'] = SolicitacaoDisciplina.objects.filter(status='F')
        context['status'] = 'A'

        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context

class SolicitacaoDisciplinaPendentesAcademicoListView(ListView, GroupRequiredMixin): 
    model = SolicitacaoDisciplina
    template_name = 'SistemaDeSolicitacoes/disciplina_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = u"Acadêmico"

    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='P').filter(professor_responsavel__icontains=search) | queryset.filter(status='P').filter(nome_disciplina__icontains=search) 
        else:
            return queryset.filter(status='P')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoDisciplinaPendentesAcademicoListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoDisciplina.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoDisciplina.objects.filter(status='E')
        context['pendentes'] = SolicitacaoDisciplina.objects.filter(status='P')
        context['fechadas'] = SolicitacaoDisciplina.objects.filter(status='F')
        context['status'] = 'P'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context

class SolicitacaoDisciplinaEncerradasListView(ListView, GroupRequiredMixin): 
    model = SolicitacaoDisciplina
    template_name = 'SistemaDeSolicitacoes/disciplina_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = [u"Acadêmico", u"Suporte"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='F').filter(professor_responsavel__icontains=search) | queryset.filter(status='F').filter(nome_disciplina__icontains=search) 
        else:
            return queryset.filter(status='F')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoDisciplinaEncerradasListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoDisciplina.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoDisciplina.objects.filter(status='E')
        context['pendentes'] = SolicitacaoDisciplina.objects.filter(status='P')
        context['fechadas'] = SolicitacaoDisciplina.objects.filter(status='F')
        context['status'] = 'F'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context


class SolicitacaoDisciplinaEntradaSuporteListView(ListView):
    model = SolicitacaoDisciplina
    template_name = 'SistemaDeSolicitacoes/disciplina_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = u"Suporte"


    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='E').filter(professor_responsavel__icontains=search) | queryset.filter(status='E').filter(nome_disciplina__icontains=search) 
        else:
            return queryset.filter(status='E')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoDisciplinaEntradaSuporteListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoDisciplina.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoDisciplina.objects.filter(status='E')
        context['pendentes'] = SolicitacaoDisciplina.objects.filter(status='P')
        context['fechadas'] = SolicitacaoDisciplina.objects.filter(status='F')
        context['status'] = 'E'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context

def SolicitacaoDisciplinaAcademicoDetailView(request, solicitacao_id):
    solicitacao = SolicitacaoDisciplina.objects.get(pk=solicitacao_id)
    if request.method == "POST":
        form = SolicitacaoAvaliacaoForm(request.POST)
        if form.is_valid():
            if request.POST.get('aprovar') == 'aprovar':
                if 'Acadêmico' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'A'
                ):
                    solicitacao.status = 'E'
                    # DISPARAR EMAIL SUCESSO PARA SUPORTE
                elif 'Suporte' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'E'
                ):
                    solicitacao.status = 'F'
                    # DISPARAR EMAIL DE SUCESSO PARA ACADEMICO E PROFESSOR 
            if request.POST.get('reprovar') == 'reprovar':
                if 'Acadêmico' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'A'
                ):
                    solicitacao.status = 'F'
                    # DISPARAR EMAIL DE FALHA PARA PROFESSOR
                elif 'Suporte' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'E'
                ):
                    solicitacao.status = 'P'
                    # DISPARAR EMAIL DE FALHA PARA ACADÊMICO
            nova_mensagem = MensagemDisciplina(mensagem=form.cleaned_data['mensagem'], autor=request.user.username, solicitacao_disciplina=solicitacao)
            nova_mensagem.save()
            solicitacao.save()
            return redirect('index')
            
    form = SolicitacaoAvaliacaoForm()
    context = {
        'solicitacao': solicitacao,
        'form': form,
        
    }
    return render(request, 'SistemaDeSolicitacoes/disciplina_avaliacao.html', context)


### CURSO ###

class SolicitacaoCursoCreateView(CreateView):
    form_class = SolicitacaoCursoForm
    template_name = 'SistemaDeSolicitacoes/solicitacao_de_curso.html'
    success_url = 'index'

    def form_valid(self, form):
        solicitacao = form.save(commit=False)
        solicitacao.status = 'A'
        solicitacao.save()
        messages.success(self.request, 'Solicitação criada com sucesso!')
        #DISPARAR EMAIL PARA O ACADÊMICO
        new_email = SendEmail(
            subject="Nova Solicitação de Abertura de Curso | CEAD/UFJF",
            recipients=["academico.cead@ufjf.br"],
            message="""
                Uma nova solicitação de abertura de curso foi aberta por {}:

                E-mail do Responsável: {},
                Curso: {},
                Unidade de Lotação: {},
                Início do Curso: {}

                Para mais detalhes, favor acessar o Sistema de Solicitações.


                Att.,
                CEAD/UFJF
            """.format(
                form.cleaned_data['professor_responsavel'], 
                form.cleaned_data['email'],
                form.cleaned_data['nome_curso'], 
                form.cleaned_data['unidade_lotacao'],
                form.cleaned_data['curso_inicio'].strftime('%d/%m/%Y')
            )
        )
        # new_email.send()
        return redirect('index')

class SolicitacaoCursoEntradaAcademicoListView(ListView, GroupRequiredMixin):
    model = SolicitacaoCurso
    template_name = 'SistemaDeSolicitacoes/curso_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = u"Acadêmico"

    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='A').filter(professor_responsavel__icontains=search) | queryset.filter(status='A').filter(nome_curso__icontains=search) 
        else:
            return queryset.filter(status='A')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoCursoEntradaAcademicoListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoCurso.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoCurso.objects.filter(status='E')
        context['pendentes'] = SolicitacaoCurso.objects.filter(status='P')
        context['fechadas'] = SolicitacaoCurso.objects.filter(status='F')
        context['status'] = 'A'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context

class SolicitacaoCursoPendentesAcademicoListView(ListView, GroupRequiredMixin): 
    model = SolicitacaoCurso
    template_name = 'SistemaDeSolicitacoes/curso_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = u"Acadêmico"

    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='P').filter(professor_responsavel__icontains=search) | queryset.filter(status='P').filter(nome_curso__icontains=search) 
        else:
            return queryset.filter(status='P')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoCursoPendentesAcademicoListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoCurso.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoCurso.objects.filter(status='E')
        context['pendentes'] = SolicitacaoCurso.objects.filter(status='P')
        context['fechadas'] = SolicitacaoCurso.objects.filter(status='F')
        context['status'] = 'P'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context

class SolicitacaoCursoEncerradasListView(ListView, GroupRequiredMixin): 
    model = SolicitacaoCurso
    template_name = 'SistemaDeSolicitacoes/curso_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = [u"Acadêmico", u"Suporte"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='F').filter(professor_responsavel__icontains=search) | queryset.filter(status='F').filter(nome_curso__icontains=search) 
        else:
            return queryset.filter(status='F')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoCursoEncerradasListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoCurso.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoCurso.objects.filter(status='E')
        context['pendentes'] = SolicitacaoCurso.objects.filter(status='P')
        context['fechadas'] = SolicitacaoCurso.objects.filter(status='F')
        context['status'] = 'F'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context


class SolicitacaoCursoEntradaSuporteListView(ListView):
    model = SolicitacaoCurso
    template_name = 'SistemaDeSolicitacoes/curso_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = u"Suporte"


    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='E').filter(professor_responsavel__icontains=search) | queryset.filter(status='E').filter(nome_curso__icontains=search) 
        else:
            return queryset.filter(status='E')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoCursoEntradaSuporteListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoCurso.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoCurso.objects.filter(status='E')
        context['pendentes'] = SolicitacaoCurso.objects.filter(status='P')
        context['fechadas'] = SolicitacaoCurso.objects.filter(status='F')
        context['status'] = 'E'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context

def SolicitacaoCursoAcademicoDetailView(request, solicitacao_id):
    solicitacao = SolicitacaoCurso.objects.get(pk=solicitacao_id)
    if request.method == "POST":
        form = SolicitacaoAvaliacaoForm(request.POST)
        if form.is_valid():
            if request.POST.get('aprovar') == 'aprovar':
                if 'Acadêmico' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'A'
                ):
                    solicitacao.status = 'E'
                elif 'Suporte' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'E'
                ):
                    solicitacao.status = 'F'
            if request.POST.get('reprovar') == 'reprovar':
                if 'Acadêmico' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'A'
                ):
                    solicitacao.status = 'F'
                elif 'Suporte' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'E'
                ):
                    solicitacao.status = 'P'
            nova_mensagem = MensagemCurso(mensagem=form.cleaned_data['mensagem'], autor=request.user.username, solicitacao_curso=solicitacao)
            nova_mensagem.save()
            solicitacao.save()
            return redirect('index')
            
    form = SolicitacaoAvaliacaoForm()
    context = {
        'solicitacao': solicitacao,
        'form': form,
        
    }
    return render(request, 'SistemaDeSolicitacoes/curso_avaliacao.html', context)

### AUDIOVISUAL ###

class SolicitacaoAudiovisualCreateView(CreateView):
    form_class = SolicitacaoAudiovisualForm
    template_name = 'SistemaDeSolicitacoes/solicitacao_audiovisual.html'
    success_url = 'index'
    
    def form_valid(self, form):
        solicitacao = form.save(commit=False)
        solicitacao.status = 'A'
        solicitacao.save()
        messages.success(self.request, 'Solicitação criada com sucesso!')
        #DISPARAR EMAIL PARA O COORDENAÇÃO
        new_email = SendEmail(
            subject="Nova Solicitação de Uso do Estúdio | CEAD/UFJF",
            recipients=["liliane.faria@uab.ufjf.br", "wagner@uab.ufjf.br", "wagner@caed.ufjf.br"],
            message="""
                Uma nova solicitação de utilização do estúdio foi aberta por {}:

                E-mail do Responsável: {},
                Setor/Curso: {},
                Data e Horário: {},
                Breve Descrição: {}

                Para mais detalhes, favor acessar o Sistema de Solicitações.


                Att.,
                CEAD/UFJF
            """.format(
                form.cleaned_data['professor_responsavel'], 
                form.cleaned_data['email'],
                form.cleaned_data['setor_ou_curso'], 
                form.cleaned_data['data_gravacao'].strftime('%d/%m/%Y') + ' às ' + form.cleaned_data['hora_gravacao'].strftime('%H:%M'),
                form.cleaned_data['breve_descricao'],
            )
        )
        # new_email.send()
        return redirect('index')

class SolicitacaoAudiovisualEntradaCoordenacaoListView(ListView, GroupRequiredMixin):
    model = SolicitacaoAudiovisual
    template_name = 'SistemaDeSolicitacoes/audiovisual_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = u"Produção"

    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='A').filter(professor_responsavel__icontains=search) | queryset.filter(status='A').filter(setor_ou_curso__icontains=search) 
        else:
            return queryset.filter(status='A')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoAudiovisualEntradaCoordenacaoListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoAudiovisual.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoAudiovisual.objects.filter(status='E')
        context['pendentes'] = SolicitacaoAudiovisual.objects.filter(status='P')
        context['fechadas'] = SolicitacaoAudiovisual.objects.filter(status='F')
        context['status'] = 'A'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context

class SolicitacaoAudiovisualPendentesCoordenacaoListView(ListView, GroupRequiredMixin): 
    model = SolicitacaoAudiovisual
    template_name = 'SistemaDeSolicitacoes/audiovisual_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = u"Acadêmico"

    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='P').filter(professor_responsavel__icontains=search) | queryset.filter(status='P').filter(setor_ou_curso__icontains=search) 
        else:
            return queryset.filter(status='P')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoAudiovisualPendentesCoordenacaoListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoAudiovisual.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoAudiovisual.objects.filter(status='E')
        context['pendentes'] = SolicitacaoAudiovisual.objects.filter(status='P')
        context['fechadas'] = SolicitacaoAudiovisual.objects.filter(status='F')
        context['status'] = 'P'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context

class SolicitacaoAudiovisualEncerradasListView(ListView, GroupRequiredMixin): 
    model = SolicitacaoAudiovisual
    template_name = 'SistemaDeSolicitacoes/audiovisual_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = [u"Acadêmico", u"Suporte"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='F').filter(professor_responsavel__icontains=search) | queryset.filter(status='F').filter(setor_ou_curso__icontains=search) 
        else:
            return queryset.filter(status='F')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoAudiovisualEncerradasListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoAudiovisual.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoAudiovisual.objects.filter(status='E')
        context['pendentes'] = SolicitacaoAudiovisual.objects.filter(status='P')
        context['fechadas'] = SolicitacaoAudiovisual.objects.filter(status='F')
        context['status'] = 'F'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context


class SolicitacaoAudiovisualEntradaProducaoListView(ListView):
    model = SolicitacaoAudiovisual
    template_name = 'SistemaDeSolicitacoes/audiovisual_entrada.html'
    paginate_by = 15
    ordering = '-data_abertura'
    group_required = u"Suporte"


    def get_queryset(self):
        queryset = super().get_queryset()
        if(self.request.GET.get('filter')):
            search = self.request.GET.get('filter')
            return queryset.filter(status='E').filter(professor_responsavel__icontains=search) | queryset.filter(status='E').filter(setor_ou_curso__icontains=search) 
        else:
            return queryset.filter(status='E')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoAudiovisualEntradaProducaoListView, self).get_context_data(**kwargs)
        context['abertas'] = SolicitacaoAudiovisual.objects.filter(status='A')
        context['em_andamento'] = SolicitacaoAudiovisual.objects.filter(status='E')
        context['pendentes'] = SolicitacaoAudiovisual.objects.filter(status='P')
        context['fechadas'] = SolicitacaoAudiovisual.objects.filter(status='F')
        context['status'] = 'E'
        if 'Suporte' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Suporte'
        elif 'Acadêmico' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Acadêmico'
        elif 'Produção' in [group.name for group in self.request.user.groups.all()]: #type: ignore
            context['groups'] = 'Produção'
        return context

def SolicitacaoAudiovisualCoordenacaoDetailView(request, solicitacao_id):
    solicitacao = SolicitacaoAudiovisual.objects.get(pk=solicitacao_id)
    if request.method == "POST":
        form = SolicitacaoAvaliacaoForm(request.POST)
        if form.is_valid():
            if request.POST.get('aprovar') == 'aprovar':
                if 'Coordenação' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'A'
                ):
                    solicitacao.status = 'E'
                elif 'Produção' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'E'
                ):
                    solicitacao.status = 'F'
            if request.POST.get('reprovar') == 'reprovar':
                if 'Coordenação' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'A'
                ):
                    solicitacao.status = 'F'
                elif 'Produção' in [group.name for group in request.user.groups.all()] or (
                    request.user.is_superuser and solicitacao.status == 'E'
                ):
                    solicitacao.status = 'P'
            nova_mensagem = MensagemAudiovisual(mensagem=form.cleaned_data['mensagem'], autor=request.user.username, solicitacao_audiovisual=solicitacao)
            nova_mensagem.save()
            solicitacao.save()
            
            messages.success(request, 'Solicitação atualizada com sucesso!')
            
            if 'Coordenacao' in [group.name for group in request.user.groups.all()] or request.user.is_superuser:
                return redirect('audiovisual-entrada-coordenacao')
            return redirect('audiovisual-entrada-producao')
            
    form = SolicitacaoAvaliacaoForm()
    context = {
        'solicitacao': solicitacao,
        'form': form,
    }
    return render(request, 'SistemaDeSolicitacoes/audiovisual_avaliacao.html', context)