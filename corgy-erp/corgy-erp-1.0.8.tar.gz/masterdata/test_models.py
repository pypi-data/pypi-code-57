from django.test import TestCase as DjangoTestCase
from . import models

class TestCase(DjangoTestCase):

    def _test_create(self, manager):
        o = manager.create(code='code', name='name')
        self.assertEqual('code', o.code)
        self.assertEqual('name', o.name)


class ApplianceQualityTest(TestCase):

    def test_business_form_create(self):
        self._test_create(models.ApplianceQuality.objects)

class AutonomeActivityStatementTest(TestCase):

    def test_business_form_create(self):
        self._test_create(models.AutonomeActivityStatement.objects)

class BusinessFormTest(TestCase):

    def test_business_form_create(self):
        self._test_create(models.BusinessForm.objects)

class ContributionTest(TestCase):

    def test_contribution_create(self):
        self._test_create(models.Contribution.objects)

class DependenceQualityTest(TestCase):

    def test_dependent_quality_create(self):
        self._test_create(models.DependentQuality.objects)

class DependenceRightTest(TestCase):

    def test_dependent_right_create(self):
        self._test_create(models.DependentRight.objects)

class DiscountTest(TestCase):

    def setUp(self):
        self.tax = models.Tax.objects.create(code='tax-code', name="tax-name")

    def test_discount_create(self):
        o = models.Discount.objects.create(code='code', name='name', tax=self.tax)
        self.assertEqual('code', o.code)
        self.assertEqual('name', o.name)

class FamilyTaxDiscountStatementTest(TestCase):

    def test_discount_create(self):
        self._test_create(models.FamilyTaxDiscountStatement.objects)

class LegalTest(TestCase):

    def test_legal_create(self):
        self._test_create(models.Legal.objects)

class PauseCategoryTest(TestCase):

    def test_pause_category_create(self):
        self._test_create(models.PauseCategory.objects)

class PayrollModeTest(TestCase):

    def test_payroll_mode_create(self):
        self._test_create(models.PayrollMode.objects)

class PretenceTest(TestCase):

    def test_pretence_create(self):
        self._test_create(models.Pretence.objects)

class PrimeMarriageStatementTest(TestCase):

    def test_pretence_create(self):
        self._test_create(models.PrimeMarriageStatement.objects)

class SimplifiedBurdenSharingContributionTaxLimitTest(TestCase):

    def test_pretence_create(self):
        self._test_create(models.SimplifiedBurdenSharingContributionTaxLimit.objects)

class RevenueBaseTest(TestCase):

    def test_pretence_create(self):
        self._test_create(models.RevenueBase.objects)

class RevenueTypeTest(TestCase):

    def test_pretence_create(self):
        self._test_create(models.RevenueType.objects)


class TaxTest(TestCase):

    def test_tax_create(self):
        self._test_create(models.Tax.objects)

class TimesheetCategoryTest(TestCase):

    def test_time_sheet_category_create(self):
        self._test_create(models.TimeSheetCategory.objects)

class TitleTest(TestCase):

    def test_title_create(self):
        self._test_create(models.Title.objects)

class UniformBookingClassificationSystemTest(TestCase):

    def test_title_create(self):
        self._test_create(models.UniformBookingClassificationSystem.objects)
