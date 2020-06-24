from psu_base.services import utility_service
from psu_base.classes.IdentityCAS import IdentityCAS
from psu_base.classes.Log import Log
from psu_base.classes.Auth import Auth
from psu_base.models.audit import Audit
from psu_base.classes.DynamicRole import DynamicRole
from django.contrib.auth.models import User
from psu_base.classes.User import User as PSUser

log = Log()


def get_auth_object():
    return Auth(auto_resume=True)


def get_user():
    return get_auth_object().get_user()


def is_logged_in():
    return get_auth_object().is_logged_in()


def has_authority(authority_code, sso_user_only=False, require_global=False):
    return get_auth_object().has_authority(authority_code, sso_user_only=sso_user_only, require_global=require_global)


def audit_event(event_code, previous_value=None, new_value=None, comments=None):
    """Audit some important event performed by an authenticated user"""
    log.trace()

    auth = get_auth_object()
    audit_instance = Audit(
        app_code=utility_service.get_app_code(),
        username=auth.sso_user.username,
        event_code=event_code,
        previous_value=previous_value,
        new_value=new_value,
        comments=comments
    )

    # If the user is impersonating or proxying, show the proxied user
    # This may help track down how something changed for a user that did not actually perform the event
    if auth.is_impersonating():
        audit_instance.impersonated_username = auth.impersonated_user.username
    if auth.proxied_user and auth.proxied_user.is_valid():
        audit_instance.proxied_username = auth.proxied_user.username

    # Save the audit record
    audit_instance.save()


#
# REMAINING CODE IS CALLED AUTOMATICALLY. YOU SHOULDN'T CALL IT ANY OTHER WAY.
#


def set_sso_user(request):
    """Save the SSO-authenticated user into the session, or remove it if logged out"""
    auth = Auth(auto_resume=True)

    # If logged in
    if request.user.is_authenticated:
        # Put CAS attributes into more intuitively named (and auto-completable) properties
        cas_id = IdentityCAS(request)

        # Was this user already logged in?
        returning_user = auth.is_logged_in() and cas_id.equals(auth.sso_user.username)

        # If this user is already saved, no need to update it
        if not returning_user:
            log.trace()  # Only trace this on initial login
            utility_service.set_session_var('psu_base_sso_username', cas_id.username)

            # Create a new Auth object. Includes identity and authorities
            auth = Auth(cas_id.username)

            # Update Django staff/superuser permissions for access to admin pages
            try:
                django_user = User.objects.get(username=cas_id.username)
                if auth.has_authority('DynamicSuperUser'):
                    if not django_user.is_staff:
                        django_user.is_staff = 1
                        django_user.is_superuser = 1
                        django_user.save()
                else:
                    if django_user.is_staff:
                        django_user.is_staff = 0
                        django_user.is_superuser = 0
                        django_user.save()
            except Exception as ee:
                log.error("Unable to update Django user permissions")

    # If not logged in
    else:
        utility_service.set_session_var('psu_base_sso_username', None)

    auth.save()

    # Features may be Limited to administrators during testing/validation of new features
    # To avoid circular imports when checking for admin authority from utility_service, flag admins
    # in the temp session. This should remain true even while impersonating non-admins (for limited features only).
    utility_service.set_session_var(
        'allow_limited_features',
        True if has_authority(DynamicRole().power_user()) else None
    )


def look_up_user_cache(user_info):
    """
    Look up a person's Identity (not including authorities), and retain it for
    the duration of the request to allow repeat lookups without hitting Finti each time
    """
    user_info = str(user_info)
    user_map = _cached_users(user_info)
    if user_info in user_map:
        return user_map[user_info]
    else:
        return None


def _cached_users(user_info):
    user_map = utility_service.recall()
    if user_map and user_info in user_map:
        return user_map
    else:
        if type(user_map) is not dict:
            user_map = {}

        user_instance = PSUser(user_info, get_authorities=False)
        if user_instance:
            user_map[user_info] = user_instance

    return utility_service.store(user_map)
