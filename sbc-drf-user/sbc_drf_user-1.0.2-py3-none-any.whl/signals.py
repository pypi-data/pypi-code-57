#: Upon user requests the reset password
from django.dispatch import Signal

reset_password_request = Signal(providing_args=['instance', 'retry'])
#: Upon reset password process completes
reset_password_done = Signal(providing_args=['instance'])
#: Upon successful password change
password_changed = Signal(providing_args=['instance'])
#: Upon new user created and if email is unverified
user_registered = Signal(providing_args=['instance'])
