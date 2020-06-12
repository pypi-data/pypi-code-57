from django.test import TestCase
from happy_quotas.models import Quota


class QuotaTest(TestCase):
    def test_add_initial_credit(self):
        quota = Quota()
        quota.add_credits(1)
        self.assertEqual(0, quota.formerly_unused_credits)
        self.assertEqual(1, quota.current_plans_credits)
        self.assertEqual(1, quota.remaining_plan_credits)
        self.assertEqual(1, quota.quota_available)
        self.assertEqual(1, quota.quota_max)

    def test_add_two_plans(self):
        quota = Quota()
        quota.add_credits(1)
        quota.add_credits(5)
        self.assertEqual(1, quota.formerly_unused_credits)
        self.assertEqual(5, quota.current_plans_credits)
        self.assertEqual(5, quota.remaining_plan_credits)
        self.assertEqual(6, quota.quota_available)
        self.assertEqual(6, quota.quota_max)

    def test_add_and_use_credit(self):
        quota = Quota()
        quota.add_credits(1)
        quota.add_credits(5)
        quota.use_credit()
        self.assertEqual(0, quota.formerly_unused_credits)
        self.assertEqual(5, quota.current_plans_credits)
        self.assertEqual(5, quota.remaining_plan_credits)
        self.assertEqual(5, quota.quota_available)
        self.assertEqual(5, quota.quota_max)

    def test_add_plans_and_exceed_use(self):
        quota = Quota()
        quota.add_credits(1)
        quota.add_credits(5)    # total = 6
        quota.use_credit()
        quota.use_credit()
        quota.use_credit()
        quota.add_credits(12)   # total = 18, already used = 3, available = 15
        with self.assertRaises(ValueError):
            for i in range(16):
                quota.use_credit()
