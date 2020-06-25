from material.frontend.views import ModelViewSet

from . import models


class ProfileModelViewSet(ModelViewSet):
   model = models.Profile
