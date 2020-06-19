import random
import string
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from djangoldp.models import Model
from .permissions import CustomerPermissions, ProjectPermissions, ProjectMemberPermissions

from .views import ProjectMembersViewset

class Customer(Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    logo = models.URLField(blank=True, null=True)
    companyRegister = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_customers", on_delete=models.DO_NOTHING,
                              null=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    class Meta(Model.Meta):
        auto_author = 'owner'
        owner_field = 'owner'
        anonymous_perms = []
        authenticated_perms = []
        owner_perms = ['view', 'add', 'change', 'delete']
        permission_classes = [CustomerPermissions]

    def __str__(self):
        return self.name


class BusinessProvider(Model):
    name = models.CharField(max_length=255)
    fee = models.PositiveIntegerField(default='0')

    def __str__(self):
        return self.name


def auto_increment_project_number():
  last_inc = Project.objects.all().order_by('id').last()
  if not last_inc:
    return 1
  return last_inc.number + 1


MODEL_MODIFICATION_USER_FIELD = 'modification_user'
STATUS_CHOICES = [
    ('Public', 'Public'),
    ('Private', 'Private'),
    ('Archived', 'Archived'),
]


class Project(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='Private')
    number = models.PositiveIntegerField(default=auto_increment_project_number, editable=False)
    creationDate = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)  # WARN add import
    team = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Member', blank=True)
    captain = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True,
                                related_name='+')
    driveID = models.TextField(null=True, blank=True)
    businessProvider = models.ForeignKey(BusinessProvider, blank=True, null=True, on_delete=models.DO_NOTHING)
    jabberID = models.CharField(max_length=255, blank=True, null=True)
    jabberRoom = models.BooleanField(default=True)

    class Meta(Model.Meta):
        nested_fields = ['team', 'customer', 'members']
        permission_classes = [ProjectPermissions]
        anonymous_perms = []
        authenticated_perms = []
        owner_perms = []
        rdf_type = 'hd:project'

    def __str__(self):
        return self.name

    def get_admins(self):
        return self.members.filter(is_admin=True)


class Member(Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    is_admin = models.BooleanField(default=False)

    class Meta(Model.Meta):
        container_path = "project-members/"
        permission_classes = [ProjectMemberPermissions]
        anonymous_perms = []
        authenticated_perms = ['view', 'add']
        owner_perms = ['inherit']
        unique_together = ['user', 'project']
        rdf_type = 'hd:projectmember'
        view_set = ProjectMembersViewset

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.user:
            if self.user.username == "hubl-workaround-493":
                self.user = None

        # cannot be duplicated Members
        if not self.pk and Member.objects.filter(project=self.project, user=self.user).exists():
            return

        super(Member, self).save(*args, **kwargs)

@receiver(post_save, sender=Member)
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


@receiver(pre_save, sender=Project)
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


@receiver(post_save, sender=Project)
def set_captain_as_member(instance, created, **kwargs):
    if instance.captain is not None:
        try:
            captain_member = instance.members.get(user=instance.captain)
            if not captain_member.is_admin:
                captain_member.is_admin = True
                captain_member.save()
        except Member.DoesNotExist:
            Member.objects.create(user=instance.captain, project=instance, is_admin=True)
