import uuid
from django.utils import timezone
from django.db import models

from SistemaDeSolicitacoes.validators import validate_is_business_time, validate_is_future

TIPO_CURSO_CHOICES = (
    ('gra', 'Graduação'),
    ('esp', 'Especialização'),
    ('mes', 'Mestrado'),
    ('dou', 'Doutorado'),
    ('ext', 'Extensão'),
    ('cur', 'Curso Livre'),
)

STATUS_CHOICES = (
        ('A', 'Aberto'),
        ('E', 'Em Andamento'),
        ('P', 'Pendente'),
        ('F', 'Fechado')
)

class SolicitacaoDisciplina(models.Model):
    # solicitante = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professor_responsavel = models.CharField(max_length=255, verbose_name="Professor Responsável")
    siape = models.CharField(max_length=7, verbose_name="SIAPE")
    email = models.EmailField(verbose_name="E-mail")
    CATEGORIA_CHOICES = (
        ('SIGA/UAB', 'Correspondência no SIGA/UAB'),
        ('SIGA/Flex', 'Correspondência no SIGA/Flexibilização Curricular'),
        ('Livre', 'Sem Correspondência no SIGA/Curso Livre')
    )
    categoria = models.CharField(max_length=9, choices=CATEGORIA_CHOICES)
    unidade_lotacao = models.CharField(max_length=50, verbose_name="Unidade de Lotação")
    codigo_siga = models.CharField(max_length=30, verbose_name="Código SIGA", blank=True, null=True)
    nome_disciplina = models.CharField(max_length=255, verbose_name="Nome da Disciplina")
    tipo_curso = models.CharField(max_length=3, choices=TIPO_CURSO_CHOICES, verbose_name="Tipo de Curso")
    # curso_disciplina = models.ForeignKey(CM_curso, on_delete=models.RESTRICT, verbose_name="A qual curso pertence a disciplina")
    curso_disciplina = models.CharField(verbose_name="Curso", max_length=255)
    departamento_disciplina = models.CharField(max_length=255, verbose_name="Departamento")
    ANO_CHOICES = (
        (timezone.now().year - 1, str(timezone.now().year - 1)),
        (timezone.now().year, str(timezone.now().year)),
        (timezone.now().year + 1, str(timezone.now().year + 1)),
    )
    ano = models.IntegerField(choices=ANO_CHOICES)
    semestre = models.CharField(max_length=1, choices=(('1','1'),('2','2'),('3','3'), ('4','4')))
    turma = models.CharField(max_length=12, verbose_name="Turma(s)")
    grupos = models.CharField(max_length=64, null=True, blank=True, verbose_name="Grupos (ex.: AB, C, ...)")
    conteudo_passado = models.CharField(max_length=255, null=True, blank=True, verbose_name="Favor informar o nome breve da disciplina a importar")
    MODO_INSCRICAO_ALUNOS_CHOICES = (
        ('ime', 'Imediatamente'),
        ('pos', 'Posteriormente'),
    )
    modo_inscricao_alunos = models.CharField(max_length=3, choices=MODO_INSCRICAO_ALUNOS_CHOICES, verbose_name="Alunos constantes na FAE (SIGA) devem ser inscritos")
    atividades_inicio = models.DateField(verbose_name="Início das atividades")
    atividades_fim = models.DateField(verbose_name="Fim das atividades")

    data_abertura = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    ultima_atualizacao = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name = "Solicitação de Disciplina"
        verbose_name_plural = "Solicitações de Disciplina"

    def __str__(self):
        return str(self.pk) + '. ' + self.nome_disciplina

class SolicitacaoCurso(models.Model):
    # solicitante = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professor_responsavel = models.CharField(max_length=255, verbose_name="Professor Responsável")
    siape = models.CharField(max_length=7, verbose_name="SIAPE")
    unidade_lotacao = models.CharField(max_length=50, verbose_name="Unidade de Lotação")
    nome_curso = models.CharField(max_length=255, verbose_name="Nome do Curso")
    email = models.EmailField(verbose_name="E-mail")
    tipo_curso = models.CharField(max_length=3, choices=TIPO_CURSO_CHOICES, verbose_name="Tipo de Curso")
    CARACTERISTICAS_CHOICES = (
        ('UAB', 'UAB'),
        ('Não UAB', 'Não UAB'),
        ('ERE', 'ERE'),
        ('Híbrido', 'Híbrido'),
        ('Gratuito', 'Gratuito')
    )
    caracteristicas = models.CharField(max_length=8, choices=CARACTERISTICAS_CHOICES, verbose_name="Características")
    qtd_disciplinas = models.PositiveIntegerField(verbose_name="Quantidade de Disciplinas")
    inscricoes_inicio = models.DateField(verbose_name="Início das Inscrições")
    inscricoes_fim = models.DateField(verbose_name="Fim das Inscrições")
    curso_inicio = models.DateField(verbose_name="Início do Curso")
    curso_fim = models.DateField(verbose_name="Fim do Curso")
    # Quantidade de Interlocutores Envolvidos
    professores = models.PositiveIntegerField()
    tutores = models.PositiveIntegerField()
    demais_colaboradores = models.PositiveIntegerField()
    alunos = models.PositiveIntegerField()
    # Tipo de Demanda Requerida
    criacao_AVA = models.BooleanField(verbose_name="Criação de AVA", default=False, blank=True)
    matricula_alunos = models.BooleanField(verbose_name="Matrícula de Alunos", default=False, blank=True)
    capacitacao_interlocutores = models.BooleanField(verbose_name="Capacitação de Interlocutores", default=False, blank=True)
    outra = models.TextField(blank=True, null=True, verbose_name="Solicitações adicionais")
    producao_material = models.BooleanField(verbose_name="Acionamento do setor de produção de material do CEAD", default=False, blank=True)
    acessoria_comunicacao = models.BooleanField(verbose_name="Assessoria de comunicação para sua divulgação", default=False, blank=True)
    ambiente_pre_formatado = models.BooleanField(
        verbose_name="Seu curso/disciplina deseja ambiente pré formatado?",
        help_text="O CEAD disponibiliza um Ambiente Modelo Pré Formatado para graduação e pós-graduação",
        default=False,
        blank=True
    )
    
    data_abertura = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    ultima_atualizacao = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return str(self.pk) + '. ' + self.nome_curso

    class Meta:
        verbose_name = "Solicitação de Curso"
        verbose_name_plural = "Solicitações de Curso"

class SolicitacaoAudiovisual(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professor_responsavel = models.CharField(max_length=255, verbose_name="Professor Responsável")
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=15, null=True, blank=True)
    data_gravacao = models.DateField(verbose_name="Data da gravação", validators=[validate_is_future])
    hora_gravacao = models.TimeField(verbose_name="Horário da gravação", validators=[validate_is_business_time])
    duracao = models.DurationField(verbose_name="Duração esperada de uso do estúdio", null=True, blank=True)
    setor_ou_curso = models.CharField(max_length=255, verbose_name="Setor/Curso")
    breve_descricao = models.TextField(verbose_name="Breve descrição (no máximo 250 caracteres)")
    equipamentos = models.CharField(max_length=255, verbose_name="De quais equipamentos irá precisar?")
    equipe = models.CharField(
        max_length=1, 
        choices=(
            ('S', 'Sim, precisaremos da equipe do CEAD'),
            ('N', 'Não, iremos utilizar a nossa própria equipe')
        ),
        verbose_name="Precisará dos nossos cinegrafistas ou virá com sua própria equipe de produção?"
    )
    pessoas = models.PositiveIntegerField(
        choices=(
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4")
        ),
        verbose_name="Quantas pessoas irão participar?"
    )

    data_abertura = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    ultima_atualizacao = models.DateTimeField(blank=True, null=True, auto_now=True)



class MensagemDisciplina(models.Model):
    mensagem = models.TextField()
    autor = models.CharField(max_length=255)
    solicitacao_disciplina = models.ForeignKey(SolicitacaoDisciplina, on_delete=models.SET_NULL, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

class MensagemCurso(models.Model):
    mensagem = models.TextField()
    autor = models.CharField(max_length=255)
    solicitacao_curso = models.ForeignKey(SolicitacaoCurso, on_delete=models.SET_NULL, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

class MensagemAudiovisual(models.Model):
    mensagem = models.TextField()
    autor = models.CharField(max_length=255)
    solicitacao_audiovisual = models.ForeignKey(SolicitacaoAudiovisual, on_delete=models.SET_NULL, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
