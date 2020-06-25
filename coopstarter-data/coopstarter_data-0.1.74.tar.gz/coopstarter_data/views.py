from djangoldp.views import LDPViewSet
from .models import Resource, Step


class ValidatedResourcesByStepViewSet(LDPViewSet):
  model = Resource

  def get_queryset(self, *args, **kwargs):
    step_id = self.kwargs['id']
    # if hasattr(self.request.user, 'mentor_profile'):
    #   target='mentor'
    # elif hasattr(self.request.user, 'entrepreneur_profile'):
    #   target='entrepreneur'
    # else:
    #   target='public'

    # Additional filter criteria: , target__value=target
    return super().get_queryset(*args, **kwargs)\
          .filter(steps__in=step_id, review__status='validated')\
          .exclude(submitter__username=self.request.user.username)

class PendingResourcesViewSet(LDPViewSet):
  model = Resource

  def get_queryset(self, *args, **kwargs):
    # Deactivating those additional filters for now.
    # , language__in=self.request.user.mentor_profile.languages.all(), fields__in=self.request.user.mentor_profile.fields.all()
    return super().get_queryset(*args, **kwargs)\
          .filter(review__status='pending')\
          .exclude(submitter__username=self.request.user.username)