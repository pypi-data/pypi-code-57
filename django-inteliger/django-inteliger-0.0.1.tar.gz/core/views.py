from django.http import JsonResponse
from django.views import View

from core.sistema import Inteliger


class InteligerView(View):
    def get(self, request, *args, **kwargs):
        Inteliger().atualizar_tempo_query()
        return JsonResponse({'status': 'Sistema atualizado com sucesso!'}, safe=False)
