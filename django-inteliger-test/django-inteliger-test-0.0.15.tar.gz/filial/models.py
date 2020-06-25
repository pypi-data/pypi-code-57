from django.db import models
import core.models


class Filial(core.models.Log):
    codigo = models.IntegerField(null=True, unique=True)
    filial = models.CharField(max_length=500, null=True)
    cnpj = models.CharField(max_length=200, null=True)

    class Meta:
        #db_table = u'"core\".\"filial"'
        db_table = 'filial'


class Servico(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)
    filial = models.ManyToManyField(Filial, through='RelacaoServicos')

    class Meta:
        #db_table = u'"core\".\"filial_servico"'
        db_table = 'filial_servico'


class RelacaoServicos(core.models.Log):
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)

    class Meta:
        #db_table = u'"core\".\"filial_relacaoservico"'
        db_table = 'filial_relacaoservico'
        unique_together = ('filial', 'servico')