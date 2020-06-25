from django.db import models
from django.core.mail import send_mail
from djangoldp.models import Model
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from djangoldp_conversation.models import Conversation, Message
from djangoldp_like.models import Like
from django.utils import timezone
from django.template import loader

class InterfaceLanguage (Model):
    code = models.CharField(max_length=2, verbose_name="ISO Code")
    name = models.CharField(max_length=64, verbose_name="Language name")
    
    def __str__(self):
        return self.name

class Country (Model):
    code = models.CharField(max_length=2, verbose_name="ISO Code")
    name = models.CharField(max_length=64, verbose_name="Country name")
    
    def __str__(self):
        return self.name

class Language (Model):
    code = models.CharField(max_length=2, verbose_name="ISO Code")
    name = models.CharField(max_length=64, verbose_name="Language name")

    def __str__(self):
        return self.name

class Organisation (Model):
    name = models.CharField(max_length=128, verbose_name="Name")
    website = models.CharField(max_length=4096, verbose_name="Website")

    def __str__(self):
        return self.name

class Step (Model):
    name = models.CharField(max_length=128, verbose_name="Name")
    order = models.IntegerField(verbose_name="Order", blank=True, null=True, default=0)
    
    class Meta:
        anonymous_perms = ['view']
        serializer_fields=["@id", "resources", "name", "order"]
        nested_fields=["resources"]
        container_path = 'steps/'
        rdf_type = 'coopstarter:step'
    
    def __str__(self):
        return self.name

class Format (Model):
    name = models.CharField(max_length=128, verbose_name="Title")

    def __str__(self):
        return self.name

class Field (Model):
    name = models.CharField(max_length=128, verbose_name="Title")

    def __str__(self):
        return self.name

class Type (Model):
    name = models.CharField(max_length=128, verbose_name="Title")

    def __str__(self):
        return self.name

class Target (Model):
    name = models.CharField(max_length=128, verbose_name="name")
    value = models.CharField(max_length=128, verbose_name="value", blank=True, null=True)

    def __str__(self):
        return self.name

class SharingCriteria (Model):
    name = models.CharField(max_length=128, verbose_name="name")
    value = models.CharField(max_length=128, verbose_name="value", blank=True, null=True)

    def __str__(self):
        return self.name


class Entrepreneur(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="entrepreneur_profile")
    organisation = models.ForeignKey(Organisation, null=True, on_delete=models.CASCADE, related_name="entrepreneurs")
    
    class Meta:
        auto_author = 'user'
        owner_field = 'user'
        owner_perms = ['inherit', 'change', 'control', 'delete']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        serializer_fields=["@id", "user", "organisation"]
        nested_fields=["user", "organisation"]
        container_path = 'entrepreneurs/'
        rdf_type = 'coopstarter:entrepreneur'
    
    def __str__(self):
        return self.user.get_full_name()

class Mentor(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="mentor_profile")
    phone = models.CharField(max_length=25, null=True, blank=True, verbose_name='Phone number')
    organisation = models.ForeignKey(Organisation, null=True, on_delete=models.CASCADE, related_name="mentors")
    country = models.ForeignKey(Country, null=True, related_name="mentors")
    languages = models.ManyToManyField(Language, blank=True)

    headline = models.CharField(max_length=256, blank=True, null=True, verbose_name='Headline or current position')
    city = models.CharField(max_length=256, blank=True, null=True, verbose_name='City')

    biography = models.TextField(blank=True, null=True, verbose_name="Tell us more about your activities")
    skills = models.TextField(blank=True, null=True, verbose_name="What skills can you share with our entrepreneurs ?")

    fields = models.ManyToManyField(Field, blank=True)

    linkedin = models.CharField(max_length=256, null=True, blank=True, verbose_name='Linkedin account')
    twitter = models.CharField(max_length=256, null=True, blank=True, verbose_name='Twitter account')
    registered_on = models.DateTimeField(default=timezone.now)

    class Meta:
        auto_author = 'user'
        serializer_fields=["@id", "phone", "headline", "biography", "city", "skills", "linkedin",\
                           "twitter", "organisation", "fields", "languages", "country"]
        nested_fields=["user", "organisation", "fields", "languages", "country"]
        container_path = 'mentors/'
        rdf_type = 'coopstarter:mentor'
        owner_field = 'user'
        owner_perms = ['inherit', 'change', 'control', 'delete']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']

    def __str__(self):
        return self.user.get_full_name()

class Review (Model):
    comment =  models.TextField(verbose_name="Comment", blank=True)
    status = models.CharField(max_length=32, choices=(('pending', 'Pending'), ('inappropriate', 'Inappropriate'), ('validated', 'Validated'), ('to_improve', 'Improvement required')), verbose_name="Resource status", blank=True, null=True)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        owner_field = 'reviewer'
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'change']
        serializer_fields=["@id", "reviewer", "comment", "status"]
        nested_fields=["reviewer"]
        owner_perms = ['inherit', 'change', 'control', 'delete']
        container_path = 'reviews/'
        rdf_type = 'coopstarter:review'

    def __str__(self):
        return self.comment

class Resource (Model):
    # Mandatory Fields
    name = models.CharField(max_length=256, verbose_name="Title")

    format = models.ForeignKey(Format, null=True, related_name='resources')
    publication_year = models.IntegerField(verbose_name="Publication Year", null=True, blank=True)
    languages = models.ManyToManyField(Language, blank=True, verbose_name="Languages", related_name='resources')
    fields = models.ManyToManyField(Field, blank=True, verbose_name="Fields", related_name='resources')
    country = models.ForeignKey(Country, null=True)
    uri = models.CharField(max_length=4086, verbose_name="Location/weblink")
    resource_author = models.CharField(max_length=256, verbose_name="Author")
    skills = models.TextField(verbose_name="Learning outcomes/skills")

    # Complementary fields
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    iframe_link = models.TextField(verbose_name="Iframe link", blank=True, null=True)
    preview_image = models.URLField(blank=True, null=True)

    # Classification Fields
    target = models.ForeignKey(Target, verbose_name="Target audience", blank=True, null=True)
    type = models.ManyToManyField(Type, blank=True, verbose_name="Type of content", related_name='resources')
    sharing = models.ForeignKey(SharingCriteria, blank=True, null=True, verbose_name="Sharing profile", related_name='resources')

    steps = models.ManyToManyField(Step, blank=True, related_name="resources")

    # Relations to other models
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='resources')
    related = models.ManyToManyField("self", blank=True)
    conversations = models.ManyToManyField(Conversation, blank=True, related_name='resources')
    likes = models.ManyToManyField(Like, blank=True, related_name='resources')
    review = models.OneToOneField(Review, blank=True, null=True, verbose_name="Associated review", related_name='resource')
 
    class Meta:
        auto_author='submitter'
        owner_field = 'submitter'
        owner_perms = ['inherit', 'change', 'control', 'delete']
        nested_fields=["format", "conversations", "steps", "languages", "fields",\
                       "type", "submitter", "related", "likes", "review", "country"]
        serializer_fields=["@id", "name", "description", "skills", "resource_author", "target", "uri", "publication_year", "format",\
                           "conversations", "steps", "languages", "fields", "country",\
                           "type", "submitter", "related", "likes", "review", "sharing", "preview_image", "iframe_link"]
        container_path = 'resources/'
        rdf_type = 'coopstarter:resource'
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']

    def __str__(self):
        return self.name

class Request (Model):
    # Mandatory Fields
    name = models.CharField(max_length=128, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    status = models.CharField(max_length=32, verbose_name="Status", choices=(('pending', 'Pending'), ('validated', 'Validated')), default="pending")
    
    language = models.ForeignKey(Language, blank=True, verbose_name="Language")
    fields = models.ManyToManyField(Field, blank=True)
    country = models.ForeignKey(Country, null=True)

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="requests")
    skills = models.TextField(verbose_name="Learning outcomes/skills")
    
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='requests')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='reviewed_requests')

    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_on']
        auto_author='submitter'
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'change']
        owner_field = 'submitter'
        serializer_fields=["@id", "name", "description", "skills", "fields", "language",\
                           "organisation", "submitter", "reviewer", "created_on", "country", "status"]
        owner_perms = ['inherit', 'change', 'control', 'delete']
        nested_fields=["language", "fields", "organisation", "submitter", "country"]
        container_path = 'requests/'
        rdf_type = 'coopstarter:request'
        
    def __str__(self):
        return self.name

class BrokenLink(Model):
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="brokenlink_submitter")
    resource = models.ForeignKey(Resource, null=True, on_delete=models.CASCADE, related_name="brokenlink_resource")
    
    class Meta:
        auto_author = 'submitter'
        owner_field = 'submitter'
        owner_perms = ['inherit', 'change', 'control', 'delete']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        serializer_fields=["@id", "submitter", "resource"]
        nested_fields=["submitter", "resource"]
        container_path = 'brokenlinks/'
        rdf_type = 'coopstarter:brokenlinks'
    

@receiver(post_save, sender=Resource)
def create_review(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False

    if created:
        if not instance.review:
            reviewInstance = Review.objects.create(resource=instance, status="pending")
            instance.review = reviewInstance
            instance.save()
    if not created:
        if instance.review:
            if instance.review.status == 'to_improve':
                review = instance.review
                review.status='pending'
                review.save()
                message_text = loader.render_to_string(
                    'emails/txt/reviewer_modification_notification.txt', 
                    {
                        'review': review,
                        'resource': instance
                    }
                )
                message_html = loader.render_to_string(
                    'emails/html/reviewer_modification_notification.html', 
                    {
                        'review': review,
                        'resource': instance
                    }
                )

                send_mail(
                    'The resource you reviewed has been modified',
                    message_text,
                    '"Knowledge Base" <kb@starter.coop>',
                    [review.reviewer.email],
                    html_message=message_html
                )

@receiver(post_save, sender=Review)
def update_review(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False

    if not created:
        if instance.resource:
            resource = instance.resource
            if instance.status == 'validated':
                subject = 'The resource you submitted has been validated !'
                message = loader.render_to_string(
                    'emails/txt/resource_validation_notification.txt', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )
                message_html = loader.render_to_string(
                    'emails/html/resource_validation_notification.html', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )
            elif instance.status == 'to_improve':
                subject = 'The resource you submitted requires some improvements'
                message = loader.render_to_string(
                    'emails/txt/resource_improvement_notification.txt', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )
                message_html = loader.render_to_string(
                    'emails/html/resource_improvement_notification.html', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )
            elif instance.status == 'inappropriate':
                subject = 'The resource you submitted is considered inappropriate'
                message = loader.render_to_string(
                    'emails/txt/resource_refusal_notification.txt', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )
                message_html = loader.render_to_string(
                    'emails/html/resource_refusal_notification.html', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )

            if instance.status != 'pending':
                send_mail(
                    subject,
                    message,
                    '"Knowledge Base" <kb@starter.coop>',
                    [resource.submitter.email],
                    html_message=message_html
                )


@receiver(post_save, sender=BrokenLink)
def sendMailToResourceSubmitter(sender, instance, created, **kwargs):
    if created:
        message_text = loader.render_to_string(
            'emails/txt/report_broken_link.txt',
            {
                'brokenlink': instance,
            }
        )

        message_html = loader.render_to_string(
            'emails/html/report_broken_link.html',
            {
                'brokenlink': instance,
            }
        )

        send_mail(
            'The resource you submitted has a brokenlink',
            message_text,
            '"Knowledge Base" <kb@starter.coop>',
            [instance.resource.submitter.email],
            html_message=message_html
        )

@receiver(post_save, sender=Mentor)
def create_mentor_profile(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False

    if created:
        staff = get_user_model().objects.filter(is_staff=True)
        for user in staff :
            message_text = loader.render_to_string(
                'emails/txt/new_mentor_subscription.txt',
                {
                    'user': user,
                    'mentor': instance,
                }
            )

            message_html = loader.render_to_string(
                'emails/html/new_mentor_subscription.html',
                {
                    'user': user,
                    'mentor': instance,
                }
            )
            send_mail(
                'New user account registration',
                message_text,
                '"Knowledge Base" <kb@starter.coop>',
                [user.email],
                html_message=message_html
            )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False

    if created:
        staff = get_user_model().objects.filter(is_staff=True)
        for user in staff :
            message_text = loader.render_to_string(
                'emails/txt/new_user_subscription.txt',
                {
                    'user': user,
                    'new_user': instance,
                }
            )

            message_html = loader.render_to_string(
                'emails/html/new_user_subscription.html',
                {
                    'user': user,
                    'new_user': instance,
                }
            )
            send_mail(
                'New user account registration',
                message_text,
                '"Knowledge Base" <kb@starter.coop>',
                [user.email],
                html_message=message_html
            )