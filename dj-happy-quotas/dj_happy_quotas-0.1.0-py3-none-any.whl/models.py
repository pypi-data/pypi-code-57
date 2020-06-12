from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Quota(models.Model):
    """Holds info on user quotas / credits for quantifiable use."""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    formerly_unused_credits = models.PositiveIntegerField(
        help_text=_("Number of credits that were left over unused from the previous credit balance "
                    "when the current plan was booked."),
        default=0,
    )
    current_plans_credits = models.PositiveIntegerField(
        help_text=_("Number of credits that have been booked by the current – i.e. most recent – plan."),
        default=0,
    )
    remaining_plan_credits = models.PositiveIntegerField(
        help_text=_("Number of credits that are currently left unused in the current plan. "
                    "Please note that 'formerly_unused_crecits' credits are used before current plan credits."),
        default=0,
    )
    quota_available = models.PositiveIntegerField(
        help_text=_("Overall available credits. Results as sum of 'formerly_unused_credits' "
                    "and 'remaining_plan_credits'."),
        default=0,
    )
    quota_max = models.PositiveIntegerField(
        help_text=_("Total sum of all leftover credits of previous plans and what's been booked in the current plan."),
        default=0,
    )

    def add_credits(self, num_credits: int):
        """Adds some new credits to the user's quota."""
        # Care about the leftover from the previous plan.
        self.formerly_unused_credits += self.remaining_plan_credits

        # Switch to the new plan's credits.
        self.current_plans_credits = num_credits
        self.remaining_plan_credits = num_credits

        self.__update_quota()

    def use_credit(self):
        """Use one credit and update all fields of the user's quota respectively."""
        # If we don't have any credits left, we can't use one.
        if self.formerly_unused_credits == 0 and self.remaining_plan_credits == 0:
            errmsg = _("User %(user)s has no credits left, thus can't use one.") % {'user': self.user_id}
            raise ValueError(errmsg)

        # If we have some leftover credits, use them up.
        if self.formerly_unused_credits > 0:
            self.formerly_unused_credits -= 1
        else:
            self.remaining_plan_credits -= 1
        self.__update_quota()

    def __update_quota(self):
        self.quota_available = self.formerly_unused_credits + self.remaining_plan_credits
        self.quota_max = self.formerly_unused_credits + self.current_plans_credits
