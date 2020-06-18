from copy import copy
from edc_constants.constants import YES, MALE
from edc_reportable import ReportablesFormValidatorMixin, GRADE3, GRADE4
from edc_utils.date import get_utcnow
from edc_form_validators import FormValidator
from dateutil.relativedelta import relativedelta


class SpecimenResultFormValidator(ReportablesFormValidatorMixin, FormValidator):

    reportable_grades = [GRADE3, GRADE4]
    reportable_reference_list_name = "my_reference_list"

    def clean(self):
        self.validate_reportable_fields()

    def validate_reportable_fields(self):

        reportables = self.reportables_cls(
            reference_list_name=self.reportable_reference_list_name,
            cleaned_data=copy(self.cleaned_data),
            gender=MALE,
            dob=get_utcnow() - relativedelta(years=25),
            report_datetime=get_utcnow(),
        )
        reportables.validate_reportable_fields()

        reportables.validate_results_abnormal_field()

        self.applicable_if(
            YES, field="results_abnormal", field_applicable="results_reportable"
        )

        reportables.validate_results_reportable_field(
            responses=self.reportable_grades)
