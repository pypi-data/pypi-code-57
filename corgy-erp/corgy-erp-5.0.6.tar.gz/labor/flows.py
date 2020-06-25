from viewflow import frontend
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from viewflow.base import this, Flow
from viewflow.flow.activation import Activation
from viewflow.flow import Start, Handler, View, If, End
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from .models import Payroll
from .views import TimesheetUpdateProcessView
import logging
from . import models


@frontend.register
class AnnounceEmploymentFlow(Flow):
    process_class = models.Employment
    process_title = _('Foglalkoztatás bejelentése')
    process_description = _('Munkavállaló foglalkoztatásának bejelentése.')

    start = (
        Start(CreateProcessView, fields=[
            'employee',
            'employer'
        ]).Permission(auto_create=True).Available(lambda user: user.pk is not None).Next(this.end)
    )

    end = End()

@frontend.register
class FireEmployeeFlow(Flow):
    process_class = models.Employment
    process_title = _('Munkaviszony megszüntetése')
    process_description = _('Munkavállaló elbocsátásnak bejelentése.')

    start = (
        Start(CreateProcessView, fields=[
            'employee',
        ]).Permission(auto_create=True).Available(lambda user: user.pk is not None).Next(this.end)
    )

    end = End()

@frontend.register
class PayrollFlow(Flow):
    process_class = models.Payroll
    process_title = _('Számfejtés')
    process_description = _('Havi bérszámfejtése.')

    summary_template = """
        <div>
            <label>{{ flow_class.process_title }}</label> 
            <label>
                <span>{{ process.current_year }}</span>
                <span>/</span>
                <span>{{ process.current_month }}</span>
            </label>    
            <label>{{ process.employer }}-{{ process.employee }}</label>
            <div>{{ process.status }}</div>
        </div>
    """

    start = (
        Start(CreateProcessView, fields = [
            'current_year',
            'current_month',
            'employee',
        ]).Permission(auto_create=True).Available(lambda user: user.pk is not None).Next(this.fill_timesheet)
    )

    fill_timesheet = (
        View(TimesheetUpdateProcessView, fields = [
            'submitted'
        ]).Permission(auto_create=True).Next(this.fill_revenue)
    )
    fill_timesheet.short_description = _('Jelenléti ív kitöltése')

    fill_revenue = (
        View(UpdateProcessView, fields=[
            'submitted'
        ]).Permission(auto_create=True).Next(this.fill_non_monetary)
    )

    fill_non_monetary = (
        View(UpdateProcessView, fields=[
            'submitted'
        ]).Permission(auto_create=True).Next(this.fill_contributions_of_employee)
    )

    fill_contributions_of_employee = (
        View(UpdateProcessView, fields=[
            'submitted'
        ]).Permission(auto_create=True).Next(this.fill_contributions_of_employer)
    )

    fill_contributions_of_employer = (
        View(UpdateProcessView, fields=[
            'submitted'
        ]).Permission(auto_create=True).Next(this.fill_tax)
    )

    fill_tax = (
        View(UpdateProcessView, fields=[
            'submitted'
        ]).Permission(auto_create=True).Next(this.fill_other_taxes)
    )

    fill_other_taxes = (
        View(UpdateProcessView, fields=[
            'submitted'
        ]).Permission(auto_create=True).Next(this.fill_blockings)
    )

    fill_blockings = (
        View(UpdateProcessView, fields=[
            'submitted'
        ]).Permission(auto_create=True).Next(this.payroll)
    )

    payroll = (
        View(UpdateProcessView, fields=[
            'submitted'
        ]).Permission(auto_create=True).Next(this.calculate)
    )

    calculate = (
        Handler(this.calculate_payroll_request).Next(this.submit)
    )

    submit = (
        Handler(this.submit_payroll_request).Next(this.end)
    )

    end = End()

    def calculate_payroll_request(self, activation: Activation):
        logging.info(_('{title}: {employer}-{employee} {current_year}/{current_month} számítása'.format(
            employer = str(activation.process.employer),
            employee = str(activation.process.employee),
            current_year = activation.process.current_year,
            current_month = activation.process.current_month,
            title = self.process_title
        )))

    def submit_payroll_request(self, activation: Activation):
        logging.info(_('{title}: {employer}-{employee} {current_year}/{current_month} feltöltése'.format(
            employer=str(activation.process.employer),
            employee=str(activation.process.employee),
            current_year=activation.process.current_year,
            current_month=activation.process.current_month,
            title=self.process_title
        )))

@frontend.register
class BatchPayrollFlow(Flow):
    process_class = Payroll
    process_title = _('Csoportos számfejtés')
    process_description = _('Havi csoportos bérszámfejtés.')