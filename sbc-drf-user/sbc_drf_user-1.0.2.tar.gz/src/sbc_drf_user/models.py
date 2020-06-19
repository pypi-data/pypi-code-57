import logging
import uuid

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Q
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import ugettext as _
from faker import Faker
from sbc_drf import errors
from sbc_drf.mixins import AddUpdateTimeModelMixin, ViewPermModelMetaMixin

from sbc_drf_user import signals
from sbc_drf_user.errors import ErrMsg

L = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a user with the given email and password.
        """
        assert email, 'Users must have an email address'

        email = self.normalize_email(email)
        last_name = extra_fields.pop('last_name', Faker().last_name())

        user = self.model(email=email, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()

        signals.user_registered.send(instance=user, sender=self.model)

        return user

    def create(self, email, password=None, **extra_fields):
        """
        Registers the user
        :param str email: email
        :param str password: Password
        :param extra_fields:
        :return user:
        :signal user_registered: user instance
        """
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.update(is_superuser=True)

        return self._create_user(email, password, **extra_fields)

    def generate_password_reset_key(self, email):
        """
        Generates password reset key using UUID

        :param str email: Email address
        :signal reset_password_request:
        """
        try:
            user = self.get(email=self.normalize_email(email))
        except User.DoesNotExist:
            raise errors.NotFound(*ErrMsg.EMAIL_NOT_EXISTS_1003)

        if user.is_password_reset is False:
            signals.reset_password_request.send(instance=user, retry=True, sender=self.model)
            return

        user.is_password_reset = False
        user.password_reset_requested_at = timezone.now()
        user.password_reset_key = uuid.uuid4()
        user.save(update_fields=['is_password_reset', 'password_reset_requested_at',
                                 'password_reset_key'])

        signals.reset_password_request.send(instance=user, retry=False, sender=self.model)

    def reset_password(self, email, reset_key, new_password):
        """
        Reset password using password reset key

        :param str email: user email address
        :param UUID reset_key: Password reset token
        :param str new_password: New password to be set

        :signal reset_password_request: Upon successful password change
        """
        user = self.get(email=email)

        assert str(user.password_reset_key) == reset_key, ErrMsg.EMAIL_PW_KEY_MISMATCH_1004[0]

        assert user.is_password_reset is False, ErrMsg.PW_RESET_KEY_USED_1005[0]

        user.set_password(new_password)
        # changing the key so user cannot use same key again
        user.password_reset_key = uuid.uuid4()
        user.password_reset_at = timezone.now()
        user.is_password_reset = True

        user.save(update_fields=['password', 'password_reset_key', 'password_reset_at',
                                 'is_password_reset'])

        signals.reset_password_done.send(instance=user, sender=self.model)

    def first_superuser(self):
        return self.filter(is_superuser=True).order_by('id').first()

    @classmethod
    def normalize_email(cls, email):
        return super().normalize_email(email).lower()


class UserQuerySet(QuerySet):
    def staff_users(self):
        return self.filter(Q(is_staff=True) | Q(is_superuser=True))

    def superusers(self):
        return self.filter(is_superuser=True)


class AbstractUser(AddUpdateTimeModelMixin, AbstractBaseUser, PermissionsMixin):
    """
    Class to store user profile
    """
    #: First name
    first_name = models.CharField(_('First Name'), max_length=50, default='Nameless', blank=True,
                                  db_index=True)
    #: Last name
    last_name = models.CharField(_('Last Name'), max_length=50, default='', blank=True,
                                 db_index=True)
    #: Email address
    email = models.EmailField(_('Email Address'), unique=True)
    #: Indicates if user active and allowed to login
    is_active = models.BooleanField(_('active'), default=True)
    #: Indicates if the user is member of staff (who is supposed to manage various modules)
    is_staff = models.BooleanField(_('Staff'), default=False)
    #: Should be used to when user sign-up is publicly available and email verification is required.
    email_verification_key = models.UUIDField(blank=True, default=uuid.uuid4, editable=False)
    #: Password rest token when user forgot their password.
    password_reset_key = models.UUIDField(blank=True, default=uuid.uuid4, editable=False)
    #: Stores boolean if the password is reset using the key. The idea of keeping this variable
    #: is to check if the new password reset key should be generated each time user requests or it
    #: should be generated only if old key is not used. I thought it this way because sometimes
    #: email gets delayed and user keep trying and then all email contains different key that
    #: makes user confused which key should be used to reset password.
    is_password_reset = models.BooleanField(blank=True, default=True)
    #: Date time that holds the last time stamp of password reset done successfully
    password_reset_requested_at = models.DateTimeField(default=None, null=True)
    #: Date time that holds the last time stamp of password reset done successfully
    password_reset_at = models.DateTimeField(default=None, null=True)
    #: Removing unwanted fields
    last_login = None

    objects = UserManager.from_queryset(UserQuerySet)()

    USERNAME_FIELD = 'email'

    class Meta(AbstractBaseUser.Meta, ViewPermModelMetaMixin):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'user'
        abstract = True

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def short_name(self):
        return self.first_name

    def change_password(self, new_password, **kw):
        """
        Helper method to user change password

        :param str new_password: New password
        :send signal: password_changed
        """
        L.debug('Changing password')

        self.set_password(new_password)
        self.save()

        signals.password_changed.send(instance=self, sender=self.__class__)

    # On Python 3: def __str__(self):
    def __str__(self):
        return self.email


class User(AbstractUser):
    pass
