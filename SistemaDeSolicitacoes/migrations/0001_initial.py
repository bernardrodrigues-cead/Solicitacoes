# Generated by Django 4.1.1 on 2022-09-08 17:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitacaoCurso',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('professor_responsavel', models.CharField(max_length=255, verbose_name='Professor Responsável')),
                ('siape', models.CharField(max_length=7, verbose_name='SIAPE')),
                ('unidade_lotacao', models.CharField(max_length=50, verbose_name='Unidade de Lotação')),
                ('nome_curso', models.CharField(max_length=255, verbose_name='Nome do Curso')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('tipo_curso', models.CharField(choices=[('gra', 'Graduação'), ('esp', 'Especialização'), ('mes', 'Mestrado'), ('dou', 'Doutorado'), ('ext', 'Extensão'), ('cur', 'Curso Livre')], max_length=3, verbose_name='Tipo de Curso')),
                ('caracteristicas', models.CharField(choices=[('UAB', 'UAB'), ('Não UAB', 'Não UAB'), ('ERE', 'ERE'), ('Híbrido', 'Híbrido'), ('Gratuito', 'Gratuito')], max_length=8, verbose_name='Características')),
                ('qtd_disciplinas', models.PositiveIntegerField(verbose_name='Quantidade de Disciplinas')),
                ('inscricoes_inicio', models.DateField(verbose_name='Início das Inscrições')),
                ('inscricoes_fim', models.DateField(verbose_name='Encerramento das Inscrições')),
                ('curso_inicio', models.DateField(verbose_name='Início do Curso')),
                ('curso_fim', models.DateField(verbose_name='Encerramento do Curso')),
                ('professores', models.PositiveIntegerField()),
                ('tutores', models.PositiveIntegerField()),
                ('demais_colaboradores', models.PositiveIntegerField()),
                ('alunos', models.PositiveIntegerField()),
                ('criacao_AVA', models.BooleanField(blank=True, default=False, verbose_name='Criação de AVA')),
                ('matricula_alunos', models.BooleanField(blank=True, default=False, verbose_name='Matrícula de Alunos')),
                ('capacitacao_interlocutores', models.BooleanField(blank=True, default=False, verbose_name='Capacitação de Interlocutores')),
                ('outra', models.TextField(blank=True, null=True, verbose_name='Solicitações adicionais')),
                ('producao_material', models.BooleanField(blank=True, default=False, verbose_name='Acionamento do setor de produção de material do CEAD')),
                ('assessoria_comunicacao', models.BooleanField(blank=True, default=False, verbose_name='Assessoria de comunicação para sua divulgação')),
                ('ambiente_pre_formatado', models.BooleanField(blank=True, default=False, help_text='O CEAD disponibiliza um Ambiente Modelo Pré Formatado para graduação e pós-graduação', verbose_name='Seu curso/disciplina deseja ambiente pré formatado?')),
                ('data_abertura', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('A', 'Aberto'), ('E', 'Em Andamento'), ('P', 'Pendente'), ('F', 'Fechado')], max_length=1)),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Solicitação de Curso',
                'verbose_name_plural': 'Solicitações de Curso',
            },
        ),
        migrations.CreateModel(
            name='SolicitacaoDisciplina',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('professor_responsavel', models.CharField(max_length=255, verbose_name='Professor Responsável')),
                ('siape', models.CharField(max_length=7, verbose_name='SIAPE')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('categoria', models.CharField(choices=[('SIGA/UAB', 'Correspondência no SIGA/UAB'), ('SIGA/Flex', 'Correspondência no SIGA/Flexibilização Curricular'), ('Livre', 'Sem Correspondência no SIGA/Curso Livre')], max_length=9)),
                ('unidade_lotacao', models.CharField(max_length=50, verbose_name='Unidade de Lotação')),
                ('codigo_siga', models.CharField(blank=True, max_length=30, null=True, verbose_name='Código SIGA')),
                ('nome_disciplina', models.CharField(max_length=255, verbose_name='Nome da Disciplina')),
                ('tipo_curso', models.CharField(choices=[('gra', 'Graduação'), ('esp', 'Especialização'), ('mes', 'Mestrado'), ('dou', 'Doutorado'), ('ext', 'Extensão'), ('cur', 'Curso Livre')], max_length=3, verbose_name='Tipo de Curso')),
                ('curso_disciplina', models.CharField(max_length=255, verbose_name='Curso')),
                ('departamento_disciplina', models.CharField(max_length=255, verbose_name='Departamento')),
                ('ano', models.CharField(max_length=4)),
                ('semestre', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1)),
                ('turma', models.CharField(max_length=12, verbose_name='Turma(s)')),
                ('grupos', models.CharField(blank=True, max_length=64, null=True, verbose_name='Grupos (ex.: AB, C, ...)')),
                ('conteudo_passado', models.CharField(blank=True, max_length=255, null=True, verbose_name='Favor informar o nome breve da disciplina a importar')),
                ('modo_inscricao_alunos', models.CharField(choices=[('ime', 'Imediatamente'), ('pos', 'Posteriormente')], max_length=3, verbose_name='Alunos constantes na FAE (SIGA) devem ser inscritos')),
                ('atividades_inicio', models.DateField(verbose_name='Início das atividades')),
                ('atividades_fim', models.DateField(verbose_name='Encerramento das atividades')),
                ('data_abertura', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('A', 'Aberto'), ('E', 'Em Andamento'), ('P', 'Pendente'), ('F', 'Fechado')], max_length=1)),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Solicitação de Disciplina',
                'verbose_name_plural': 'Solicitações de Disciplina',
            },
        ),
    ]
