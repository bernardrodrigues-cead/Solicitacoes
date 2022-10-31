from django.urls import path
from SistemaDeSolicitacoes import views

urlpatterns = [
    path('index', views.Index, name='index'),
    path('solicitacao_de_disciplina', views.SolicitacaoDisciplinaCreateView.as_view(), name='disciplina-create'),
    path('solicitacao_de_disciplina/entrada/academico', views.SolicitacaoDisciplinaEntradaAcademicoListView.as_view(), name='disciplina-entrada-academico'),
    path('solicitacao_de_disciplina/pendentes/academico', views.SolicitacaoDisciplinaPendentesAcademicoListView.as_view(), name='disciplina-pendentes-academico'),
    path('solicitacao_de_disciplina/entrada/suporte', views.SolicitacaoDisciplinaEntradaSuporteListView.as_view(), name='disciplina-entrada-suporte'),
    path('solicitacao_de_disciplina/encerradas', views.SolicitacaoDisciplinaEncerradasListView.as_view(), name='disciplina-encerradas'),
    path('solicitacao_de_curso', views.SolicitacaoCursoCreateView.as_view(), name='curso-create'),
    path('avaliacao_de_disciplina/<str:solicitacao_id>', views.SolicitacaoDisciplinaAcademicoDetailView, name='disciplina-avaliacao'),

    path('solicitacao_de_curso', views.SolicitacaoCursoCreateView.as_view(), name='curso-create'),
    path('solicitacao_de_curso/entrada/academico', views.SolicitacaoCursoEntradaAcademicoListView.as_view(), name='curso-entrada-academico'),
    path('solicitacao_de_curso/pendentes/academico', views.SolicitacaoCursoPendentesAcademicoListView.as_view(), name='curso-pendentes-academico'),
    path('solicitacao_de_curso/entrada/suporte', views.SolicitacaoCursoEntradaSuporteListView.as_view(), name='curso-entrada-suporte'),
    path('solicitacao_de_curso/encerradas', views.SolicitacaoCursoEncerradasListView.as_view(), name='curso-encerradas'),
    path('solicitacao_de_curso', views.SolicitacaoCursoCreateView.as_view(), name='curso-create'),
    path('avaliacao_de_curso/<str:solicitacao_id>', views.SolicitacaoCursoAcademicoDetailView, name='curso-avaliacao'),

    path('solicitacao_audiovisual', views.SolicitacaoAudiovisualCreateView.as_view(), name='audiovisual-create'),
    path('solicitacao_audiovisual/entrada/coordenacao', views.SolicitacaoAudiovisualEntradaCoordenacaoListView.as_view(), name='audiovisual-entrada-coordenacao'),
    path('solicitacao_audiovisual/pendentes/coordenacao', views.SolicitacaoAudiovisualPendentesCoordenacaoListView.as_view(), name='audiovisual-pendentes-coordenacao'),
    path('solicitacao_audiovisual/entrada/producao', views.SolicitacaoAudiovisualEntradaProducaoListView.as_view(), name='audiovisual-entrada-producao'),
    path('solicitacao_audiovisual/encerradas', views.SolicitacaoAudiovisualEncerradasListView.as_view(), name='audiovisual-encerradas'),
    path('avaliacao_audiovisual/<str:solicitacao_id>', views.SolicitacaoAudiovisualCoordenacaoDetailView, name='audiovisual-avaliacao'),
]