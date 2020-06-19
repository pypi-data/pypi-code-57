from django.utils.translation import ugettext as _
from sbc_drf.errors import ErrorMessage


class ErrMsg(ErrorMessage):
    # Prefixed 10

    EMAIL_EXIST_1001 = _("User with that email address already exists"), 1001
    MISMATCH_OLD_PWD_1002 = _("Current password does not match"), 1002
    EMAIL_NOT_EXISTS_1003 = _("If you have submitted a valid email address, "
                              "you will receive a link to reset your password"), 1003
    EMAIL_PW_KEY_MISMATCH_1004 = _("Invalid password reset token"), 1004
    PW_RESET_KEY_USED_1005 = _("Password reset token already used"), 1005
