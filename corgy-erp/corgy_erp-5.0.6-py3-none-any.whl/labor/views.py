from material.frontend.views import ModelViewSet, CreateModelView, UpdateModelView, DetailModelView
from material import LayoutMixin, Layout, Fieldset, Column, Row
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from django.utils.translation import ugettext_lazy as _

from . import models

#@login_required
def add_dependence(request, employmee_pk):
    employee = get_object_or_404(models.Employment, pk=employee_pk)
    form = forms.ChangeSalaryForm(employee=employee, data=request.POST or None)

    if form.is_valid():
        form.save()

    salaries = employee.salary_set.all().order_by('from_date')
    salary_data = {
        'labels': [salary.from_date.strftime('%Y-%m-%d') for salary in salaries],
        'datasets': [
            {'data': [salary.salary for salary in salaries], 'label': ugettext('Salary History')}
        ]
    }

    return render(request, 'employees/change_salary.html', {
        'form': form,
        'employee': employee,
        'salary_history': json.dumps(salary_data),
        'model': models.Employee
    })


class EmploymentModelViewSet(ModelViewSet):
    model = models.Employment
    list_display = ['pk', 'employer', 'employee', 'current_salary']

    def current_salary(self, obj):
        # salary = obj.salary_set.current()
        # return salary.salary if salary is not None else 0
        return 0
    current_salary.short_description = _('Bér')

# class SalaryDetailView(LayoutMixin, DetailModelView):
#     model = models.Salary
#
#     layout = Layout(
#         Fieldset(
#             _('Idő adatok'),
#             Row('period_month'),
#         ),
#         Fieldset(
#             _('Naptár'),
#             Row('period_year'),
#         ),
#     )

class SalaryModelViewSet(ModelViewSet):
    model = models.Salary
    list_display = ['pk', 'period_year', 'period_month', 'employee', 'salary']

    layout = Layout(
        Fieldset(
            _('Idő adatok'),
            Row('employee'),
        ),
        Fieldset(
            _('Naptár'),
            Row('employee'),
        ),
    )

# class EmployeeViewSet(ModelViewSet):
#     model = models.Employee
#     list_display = ('emp_no', 'first_name', 'last_name', 'birth_date', 'current_salary')
#
#     change_salary_view = [
#         r'^(?P<employee_pk>.+)/change_salary/$',
#         change_salary,
#         '{model_name}_change_salary'
#     ]
#
#     change_title_view = [
#         r'^(?P<employee_pk>.+)/change_title/$',
#         change_title,
#         '{model_name}_change_title'
#     ]
#
#     def current_salary(self, obj):
#         salary = obj.salary_set.current()
#         return salary.salary if salary is not None else 0
#     current_salary.short_description = _('current salary')

class TimesheetUpdateProcessView(UpdateProcessView):
    pass