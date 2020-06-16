from material.frontend.views import ModelViewSet
from viewflow.flow.views import CreateProcessView, UpdateProcessView

from . import models


class EmployeeModelViewSet(ModelViewSet):
    model = models.Employee

class TimesheetUpdateProcessView(UpdateProcessView):
    pass