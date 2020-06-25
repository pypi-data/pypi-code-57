from __future__ import annotations

from typing import Optional

import log.models
from core.models import Tipo


class InteligerMeta(type):
    _instance: Optional[Inteliger] = None

    def __call__(self) -> Inteliger:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Inteliger(metaclass=InteligerMeta):
    def __init__(self):
        self.__tempo_pesquisa = 0
        self.atualizar_tempo_query()

    def salvar_log(self, request=None, response=None):
        if request.META.get('REMOTE_ADDR') != '127.0.0.1':
            log.models.Log(
                status_code=response.status_code,
                reason_phrase=response.reason_phrase,
                metodo=request.method,
                ip=request.META.get('REMOTE_ADDR'),
                path=request.path,
                session_key=request.session.session_key,
                body=str(request.body),
            ).save()

    def atualizar_tempo_query(self):
        tempo = Tipo.objects.values('nome').filter(tipo='SISTEMA.TEMPO_QUERY').order_by('-dat_insercao').first()
        try:
            self.tempo_pesquisa = int(tempo['nome']) if tempo is not None else 0
        except:
            pass

    @property
    def tempo_pesquisa(self):
        return self.__tempo_pesquisa

    @tempo_pesquisa.setter
    def tempo_pesquisa(self, tempo):
        self.__tempo_pesquisa = tempo
