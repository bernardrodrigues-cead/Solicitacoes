from django import forms

from SistemaDeSolicitacoes.models import SolicitacaoAudiovisual, SolicitacaoCurso, SolicitacaoDisciplina

class SolicitacaoDisciplinaForm(forms.ModelForm):
    criar_grupos = forms.ChoiceField(
        choices=((0, 'Não'), (1, 'Sim')), 
        label="As turmas devem ser separadas por grupos?", 
        initial=0, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    importar_conteudo_passado = forms.ChoiceField(
        choices=((0, 'Não'), (1, 'Sim')),
        label="É necessário importar conteúdo de períodos passados?", 
        initial=0,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = SolicitacaoDisciplina
        fields = [
            'professor_responsavel',
            'siape',
            'email',
            'unidade_lotacao',
            'codigo_siga',
            'nome_disciplina',
            'categoria',
            'curso_disciplina',
            'departamento_disciplina',
            'tipo_curso',
            'ano',
            'semestre',
            'turma',
            'grupos',
            'conteudo_passado',
            'modo_inscricao_alunos',
            'atividades_inicio',
            'atividades_fim'
        ]
        widgets = {
            'professor_responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do professor responsável pela disciplina'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail para contato'}),
            'siape': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(apenas números)'}),
            'nome_disciplina': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo da disciplina'}),
            'codigo_siga': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: UABADM032'}),
            
            'curso_disciplina': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do curso ao qual a disciplina pertence'}),
            'departamento_disciplina': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departamento do curso'}),
            'unidade_lotacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidade de Lotação do curso'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'tipo_curso': forms.Select(attrs={'class': 'form-select'}),

            'atividades_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'atividades_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'modo_inscricao_alunos': forms.Select(attrs={'class': 'form-select'}),
            'ano': forms.Select(attrs={'class': 'form-select'}),
            'semestre': forms.Select(attrs={'class': 'form-select'}),
            'turma': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: A, B, C...'}),

            'criar_grupos': forms.Select(attrs={'class': 'form-select'}),
            'grupos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Grupos (ex.: AB, C, ...)',
                'style': 'display: none;'
            }),
            'conteudo_passado': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Favor informar o nome breve da disciplina a importar',
                'style': 'display: none;'
            }),
        }

class SolicitacaoCursoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoCurso
        fields = [
            'professor_responsavel',
            'siape',
            'unidade_lotacao',
            'nome_curso',
            'email',
            'tipo_curso',
            'caracteristicas',
            'qtd_disciplinas',
            'inscricoes_inicio',
            'inscricoes_fim',
            'curso_inicio',
            'curso_fim',
            # Quantidade de Interlocutores Envolvidos
            'professores',
            'tutores',
            'demais_colaboradores',
            'alunos',
            # Tipo de Demanda Requerida
            'criacao_AVA',
            'matricula_alunos',
            'capacitacao_interlocutores',
            'outra',
            'producao_material',
            'acessoria_comunicacao',
            'ambiente_pre_formatado'
        ]
        widgets = {
            'professor_responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do professor responsável'}),
            'siape': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(apenas números)'}),
            'nome_curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do curso para abertura'}),
            'unidade_lotacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidade de lotação do curso'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail para contato'}),
            'tipo_curso': forms.Select(attrs={'class': 'form-select'}),
            'caracteristicas': forms.Select(attrs={'class': 'form-select'}),
            'qtd_disciplinas': forms.NumberInput(attrs={'class': 'form-control'}),
            'inscricoes_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'inscricoes_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'curso_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'curso_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'professores': forms.NumberInput(attrs={'class': 'form-control'}),
            'tutores': forms.NumberInput(attrs={'class': 'form-control'}),
            'demais_colaboradores': forms.NumberInput(attrs={'class': 'form-control'}),
            'alunos': forms.NumberInput(attrs={'class': 'form-control'}),
            'criacao_AVA': forms.Select(
                attrs={'class': 'form-select'},
                choices=((False, 'Não'), (True, 'Sim'))
            ),
            'matricula_alunos': forms.Select(
                attrs={'class': 'form-select'},
                choices=((False, 'Não'), (True, 'Sim'))
            ),
            'capacitacao_interlocutores': forms.Select(
                attrs={'class': 'form-select'},
                choices=((False, 'Não'), (True, 'Sim'))
            ),
            'outra': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'producao_material': forms.Select(
                attrs={'class': 'form-select'},
                choices=((False, 'Não'), (True, 'Sim'))
            ),
            'acessoria_comunicacao': forms.Select(
                attrs={'class': 'form-select'},
                choices=((False, 'Não'), (True, 'Sim'))
            ),
            'ambiente_pre_formatado': forms.Select(
                attrs={'class': 'form-select'},
                choices=((False, 'Não'), (True, 'Sim'))
            )
        }

class SolicitacaoAudiovisualForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoAudiovisual
        fields = [
            'professor_responsavel',
            'email',
            'telefone',
            'data_gravacao',
            'hora_gravacao',
            'duracao',
            'setor_ou_curso',
            'breve_descricao',
            'equipamentos',
            'equipe',
            'pessoas'
        ]
        widgets = {
            'professor_responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do professor responsável'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail do professor responsável'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DDD e número'}),
            'data_gravacao': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_gravacao': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duracao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0h00 (campo não obrigatório)'}),
            'setor_ou_curso': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Setor ou Curso responsável pela solicitação'}),
            'breve_descricao': forms.Textarea(attrs={
                'rows': '6',
                'class': 'form-control', 
                'maxlength': '250',
                'placeholder': 'Fale um pouco sobre o seu projeto ou disciplina. Como podemos ajudar? Qual a finalidade da gravação?'
            
            }),
            'equipamentos': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}, choices=(
                ('Câmera', 'Câmera'),
                ('Tripé', 'Tripé'),
                ('Luzes', 'Luzes'),
                ('Microfone', 'Microfone'),
                ('Slide', 'Slide'),
                ('Teleprompter', 'Teleprompter'),
            )),
            'equipe': forms.Select(attrs={'class': 'form-select'}),
            'pessoas': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            )
        }

class SolicitacaoAvaliacaoForm(forms.Form):
    mensagem = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control w-50',
            'placeholder': 'Deixe um feedback para o solicitante',
            'rows': '4'
        }))
