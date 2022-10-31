from django.contrib import admin

from SistemaDeSolicitacoes.models import *

# Register your models here.
admin.site.register(
    (
        SolicitacaoCurso, 
        SolicitacaoDisciplina,
        SolicitacaoAudiovisual,
        MensagemDisciplina
    )
)