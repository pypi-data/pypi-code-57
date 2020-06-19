import json

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action

from remo_app.remo.models import Dataset
from remo_app.remo.services.uploads import uploads


class UploadsStatus(viewsets.GenericViewSet):

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        dataset_id = data.get('dataset_id')
        user = request.user
        dataset = Dataset.objects.filter(id=dataset_id, user=user).first()

        if not dataset or dataset.is_public and not user.is_superuser:
            return JsonResponse({
                'error': 'Only admin can upload data to public datasets.'
            }, status=status.HTTP_403_FORBIDDEN)

        session = uploads.get_or_create_session(dataset=dataset, user=user)
        return JsonResponse(session.to_dict(), status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        sessions = uploads.list_sessions()
        result = list(map(lambda item: item.to_dict(), sessions))
        return JsonResponse({'results': result})

    @action(['get'], detail=True, url_path='status')
    def status(self, request, *args, **kwargs):
        session_id = kwargs['pk']
        session = uploads.get_session(session_id)
        if not session:
            return JsonResponse({'error': f'session_id: {session_id} was not found'}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(session.to_dict())

    @action(['post'], detail=True, url_path='complete')
    def complete(self, request, *args, **kwargs):
        session_id = kwargs['pk']
        ok = uploads.start_session(session_id)
        response_status = status.HTTP_200_OK if ok else status.HTTP_404_NOT_FOUND
        return JsonResponse({'session_id': session_id}, status=response_status)

