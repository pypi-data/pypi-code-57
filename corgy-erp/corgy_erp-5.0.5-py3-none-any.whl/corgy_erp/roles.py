from rolepermissions.roles import AbstractUserRole
from django.utils.translation import ugettext_lazy as _


class Common(AbstractUserRole):
    """
    Alap szerepkör, bárki
    """
    role_name = _('Felhasználó szerepkör')
    available_permissions = {

    }

class HumanResource(AbstractUserRole):
    """
    Emberi erőforrás kezelő, felhasználó
    """
    role_name = _('Emberi erőforrás kezelő szerepkör')
    available_permissions = {
    }

class Finance(AbstractUserRole):
    """
    Pénzügyes szerepkör, felhasználó
    """
    role_name = _('Pénzügyes szerepkör')
    available_permissions = {
    }

class Employee(AbstractUserRole):
    """
    Alkalmazott szerepkör, felhasználó
    """
    role_name = _('Alkalmazott szerepkör')
    available_permissions = {
    }


class Accountant(AbstractUserRole):
    """
    Könyvelő szerepkör, személyzet
    """
    role_name = _('Könyvelő szerepkör')
    available_permissions = {
    }

class Payroller(AbstractUserRole):
    """
    Bérszámfejtő szerepkör, személyzet
    """
    role_name = _('Bérszámfejtő szerepkör')
    available_permissions = {
    }

class Leader(AbstractUserRole):
    """
    Vezető szerepkör, személyzet
    """
    role_name = _('Vezető szerepkör')
    available_permissions = {
        'can_add_module': False,
        'can_change_module': False,
        'can_delete_module': False,
        'can_view_module': True,

        'can_add_process': False,
        'can_change_process': False,
        'can_delete_process': False,
        'can_view_process': True,

        'can_add_task': True,
        'can_change_task': True,
        'can_delete_task': False,
        'can_view_task': True,

        'can_manage_process': True,

        'can_add_logentry': False,
        'can_change_logentry': True,
        'can_delete_logentry': False,
        'can_view_logentry': True,

        'can_add_permission': False,
        'can_change_permission': False,
        'can_delete_permission': False,
        'can_view_permission': False,

        'can_add_group': True,
        'can_change_group': True,
        'can_delete_group': True,
        'can_view_group': True,

        'can_add_user': True,
        'can_change_user': True,
        'can_delete_user': True,
        'can_view_user': True,

        'can_add_contenttype': False,
        'can_change_contenttype': False,
        'can_delete_contenttype': False,
        'can_view_contenttype': True,

        'can_add_session': False,
        'can_change_session': False,
        'can_delete_session': False,
        'can_view_session': True,

        'can_add_site': False,
        'can_change_site': False,
        'can_delete_site': False,
        'can_view_site': True,

        'can_add_flatpage': True,
        'can_change_flatpage': True,
        'can_delete_flatpage': True,
        'can_view_flatpage': True,

        'can_add_redirect': True,
        'can_change_redirect': True,
        'can_delete_redirect': True,
        'can_view_redirect': True,

        'can_add_address': True,
        'can_change_address': True,
        'can_delete_address': True,
        'can_view_address': True,

        'can_add_country': True,
        'can_change_country': True,
        'can_delete_country': True,
        'can_view_country': True,

        'can_add_locality': True,
        'can_change_locality': True,
        'can_delete_locality': True,
        'can_view_locality': True,

        'can_add_state': True,
        'can_change_state': True,
        'can_delete_state': True,
        'can_view_state': True,

        'can_add_avatar': True,
        'can_change_avatar': True,
        'can_delete_avatar': True,
        'can_view_avatar': True,

        'can_change_timesheetitem': True,
        'can_delete_timesheetitem': True,
        'can_view_timesheetitem': True,

        'can_add_pause': True,
        'can_change_pause': True,
        'can_delete_pause': True,
        'can_view_pause': True,

        'can_add_discount': True,
        'can_change_discount': True,
        'can_delete_discount': True,
        'can_view_discount': True,

        'can_add_customer': True,
        'can_change_customer': True,
        'can_delete_customer': True,
        'can_view_customer': True,

        'can_add_unsubscriptionprocess': True,
        'can_change_unsubscriptionprocess': True,
        'can_delete_unsubscriptionprocess': True,
        'can_view_unsubscriptionprocess': True,
        'can_manage_unsubscriptionprocess': True,
        'can_start_unsubscriptionprocess': True,

        'can_add_subscriptionprocess': True,
        'can_change_subscriptionprocess': True,
        'can_delete_subscriptionprocess': True,
        'can_view_subscriptionprocess': True,
        'can_manage_subscriptionprocess': True,
        'can_start_subscriptionprocess': True,

        'can_add_organization': True,
        'can_change_organization': True,
        'can_delete_organization': True,
        'can_view_organization': True,

        'can_add_individual': True,
        'can_change_individual': True,
        'can_delete_individual': True,
        'can_view_individual': True,

        'can_add_employment': True,
        'can_change_employment': True,
        'can_delete_employment': True,
        'can_view_employment': True,
        'can_manage_employment': True,
        'can_start_employment': True,

        'can_add_payroll': True,
        'can_change_payroll': True,
        'can_delete_payroll': True,
        'can_view_payroll': True,
        'can_manage_payroll': True,
        'can_start_payroll': True,
        'can_fill_timesheet_payroll': True,
        'can_fill_revenue_payroll': True,
        'can_payroll_payroll': True,

        'can_add_dependence': True,
        'can_change_dependence': True,
        'can_delete_dependence': True,
        'can_view_dependence': True,

        'can_add_activity': False,
        'can_change_activity': False,
        'can_delete_activity': False,
        'can_view_activity': True,

        'can_add_lead': False,
        'can_change_lead': False,
        'can_delete_lead': False,
        'can_view_lead': False,

        'can_add_ledger': True,
        'can_change_ledger': True,
        'can_delete_ledger': True,
        'can_view_ledger': True,
    }
