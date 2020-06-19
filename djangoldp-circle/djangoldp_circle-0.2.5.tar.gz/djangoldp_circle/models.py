import random
import string
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from djangoldp.models import Model
from .permissions import CirclePermissions, CircleMemberPermissions
from .views import CircleMembersViewset


MODEL_MODIFICATION_USER_FIELD = 'modification_user'
STATUS_CHOICES = [
    ('Public', 'Public'),
    ('Private', 'Private'),
    ('Archived', 'Archived'),
]


class Circle(Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    creationDate = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='Public')
    team = models.ManyToManyField(settings.AUTH_USER_MODEL, through="CircleMember", blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_circles", on_delete=models.DO_NOTHING,
                              null=True, blank=True)
    jabberID = models.CharField(max_length=255, blank=True, null=True, unique=True)
    jabberRoom = models.BooleanField(default=True)

    class Meta(Model.Meta):
        auto_author = 'owner'
        nested_fields = ["team", 'members']
        permission_classes = [CirclePermissions]
        anonymous_perms = []
        authenticated_perms = []
        owner_perms = []
        rdf_type = 'hd:circle'

    def __str__(self):
        return self.name

    def get_admins(self):
        return self.members.filter(is_admin=True)


class CircleMember(Model):
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="circles", null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    class Meta(Model.Meta):
        container_path = "circle-members/"
        permission_classes = [CircleMemberPermissions]
        anonymous_perms = []
        authenticated_perms = ['view', 'add']
        owner_perms = ['inherit']
        unique_together = ['user', 'circle']
        rdf_type = 'hd:circlemember'
        view_set = CircleMembersViewset

    def save(self, *args, **kwargs):
        if self.user:
            if self.user.username == "hubl-workaround-493":
                self.user = None
        # cannot be duplicated CircleMembers
        if not self.pk and CircleMember.objects.filter(circle=self.circle, user=self.user).exists():
            return

        super(CircleMember, self).save(*args, **kwargs)

@receiver(post_save, sender=CircleMember)
def fix_user_hubl_workaround_493(sender, instance, **kwargs):
    if not instance.user:
        try:
            request_user = getattr(instance, MODEL_MODIFICATION_USER_FIELD, None)
            if request_user is None:
                raise Exception()
            user = get_user_model().objects.get(pk=request_user.pk)
            instance.user = user
            instance.save()
        except:
            if instance.pk is not None:
                instance.delete()

@receiver(pre_save, sender=Circle)
def set_jabberid(sender, instance, **kwargs):
    if settings.JABBER_DEFAULT_HOST and not instance.jabberID:
        instance.jabberID = '{}@conference.{}'.format(
            ''.join(
                [
                    random.choice(string.ascii_letters + string.digits)
                    for n in range(12)
                ]
            ).lower(),
            settings.JABBER_DEFAULT_HOST
        )
        instance.jabberRoom = True

@receiver(post_save, sender=Circle)
def set_owner_as_member(instance, created, **kwargs):
    # add owner as an admin member
    if instance.owner is not None:
        try:
            owner_member = instance.members.get(user=instance.owner)
            if not owner_member.is_admin:
                owner_member.is_admin = True
                owner_member.save()
        except CircleMember.DoesNotExist:
            CircleMember.objects.create(user=instance.owner, circle=instance, is_admin=True)
