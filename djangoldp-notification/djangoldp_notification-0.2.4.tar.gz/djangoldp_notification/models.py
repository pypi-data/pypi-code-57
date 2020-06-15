import logging

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template import loader
from django.urls import NoReverseMatch, get_resolver
from django.utils.translation import ugettext_lazy as _
from djangoldp.fields import LDPUrlField
from djangoldp.models import Model
from threading import Thread
from djangoldp_notification.middlewares import MODEL_MODIFICATION_USER_FIELD
from djangoldp_notification.permissions import InboxPermissions, SubscriptionsPermissions


class Notification(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inbox', on_delete=models.deletion.CASCADE)
    author = LDPUrlField()
    object = LDPUrlField()
    type = models.CharField(max_length=255)
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    class Meta(Model.Meta):
        owner_field = 'user'
        ordering = ['-date']
        permission_classes = [InboxPermissions]
        anonymous_perms = ['add']
        authenticated_perms = ['inherit']
        owner_perms = ['view', 'change', 'control']

    def __str__(self):
        return '{}'.format(self.type)

    def save(self, *args, **kwargs):
        # I cannot send a notification to myself
        if self.author.startswith(settings.SITE_URL):
            try:
                # author is a WebID.. convert to local representation
                author = Model.resolve(self.author.replace(settings.SITE_URL, ''))[1]
            except NoReverseMatch:
                author = None
            if author == self.user:
                return

        super(Notification, self).save(*args, **kwargs)


class Subscription(Model):
    object = models.URLField()
    inbox = models.URLField()
    field = models.CharField(max_length=255, blank=True, null=True,
                             help_text='if set to a field name on the object model, the field will be passed instead of the object instance')

    def __str__(self):
        return '{}'.format(self.object)

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ["add", "view", "delete"]
        permission_classes = [SubscriptionsPermissions]


@receiver(post_save, sender=Subscription, dispatch_uid="nested_subscriber_check")
def create_nested_subscribers(sender, instance, created, **kwargs):
    # save subscriptions for one-to-many nested fields
    if created and not instance.is_backlink and instance.object.startswith(settings.SITE_URL):
        try:
            # object is a WebID.. convert to local representation
            local = Model.resolve(instance.object.replace(settings.SITE_URL, ''))[0]
            nested_fields = Model.get_meta(local, 'nested_fields', [])

            for nested_field in nested_fields:
                try:
                    field = local._meta.get_field(nested_field)
                    nested_container = field.related_model
                    nested_container_url = Model.absolute_url(nested_container)

                    if field.one_to_many:
                        # get the nested view set
                        nested_url = str(instance.object) + '1/' + nested_field + '/'
                        view, args, kwargs = get_resolver().resolve(nested_url.replace(settings.SITE_URL, ''))
                        # get the reverse name for the field
                        field_name = view.initkwargs['nested_related_name']

                        if field_name is not None and field_name != '':
                            # check that this nested-field subscription doesn't already exist
                            existing_subscriptions = Subscription.objects.filter(object=nested_container_url, inbox=instance.inbox,
                                                                                 field=field_name)
                            # save a Subscription on this container
                            if not existing_subscriptions.exists():
                                Subscription.objects.create(object=nested_container_url, inbox=instance.inbox, is_backlink=True,
                                                            field=field_name)
                except:
                    pass
        except:
            pass



# --- SUBSCRIPTION SYSTEM ---
@receiver(post_save, dispatch_uid="callback_notif")
@receiver(post_delete, dispatch_uid="delete_callback_notif")
def send_notification(sender, instance, **kwargs):
    if sender != Notification:
        threads = []
        recipients = []
        try:
            url_container = settings.BASE_URL + Model.container_id(instance)
            url_resource = settings.BASE_URL + Model.resource_id(instance)
        except NoReverseMatch:
            return

        # dispatch a notification for every Subscription on this resource
        for subscription in Subscription.objects.filter(models.Q(object=url_resource) | models.Q(object=url_container)):
            if not instance.is_backlink and subscription.inbox not in recipients and \
                    (not subscription.is_backlink or not kwargs.get("created")):
                # I may have configured to send the subscription to a foreign key
                if subscription.field is not None and len(subscription.field) > 1:
                    instance = getattr(instance, subscription.field, instance)
                    try:
                        url_resource = settings.BASE_URL + Model.resource_id(instance)
                    except NoReverseMatch:
                        continue

                process = Thread(target=send_request, args=[subscription.inbox, url_resource, instance,
                                                            kwargs.get("created", False)])
                process.start()
                threads.append(process)
                recipients.append(subscription.inbox)


def send_request(target, object_iri, instance, created):
    unknown = str(_("Auteur inconnu"))
    author = getattr(getattr(instance, MODEL_MODIFICATION_USER_FIELD, unknown), "urlid", unknown)
    request_type = "creation" if created else "update"

    try:
        # local inbox
        if target.startswith(settings.SITE_URL):
            user = Model.resolve_parent(target.replace(settings.SITE_URL, ''))
            Notification.objects.create(user=user, object=object_iri, type=request_type, author=author)
        # external inbox
        else:
            json = {
                "@context": settings.LDP_RDF_CONTEXT,
                "object": object_iri,
                "author": author,
                "type": request_type
            }
            requests.post(target, json=json, headers={"Content-Type": "application/ld+json"})
    except Exception as e:
        logging.error('Djangoldp_notifications: Error with request: {}'.format(e))
    return True


@receiver(post_save, sender=Notification)
def send_email_on_notification(sender, instance, created, **kwargs):
    if created and instance.summary and settings.JABBER_DEFAULT_HOST and instance.user.email:
        # get author name, and store in who
        try:
            # local author
            if instance.author.startswith(settings.SITE_URL):
                who = str(Model.resolve_id(instance.author.replace(settings.SITE_URL, '')))
            # external author
            else:
                who = requests.get(instance.author).json()['name']
        except:
            who = "Personne inconnue"

        # get identifier for resource triggering notification, and store in where
        try:
            if instance.object.startswith(settings.SITE_URL):
                where = str(Model.resolve_id(instance.object.replace(settings.SITE_URL, '')))
            else:
                where = requests.get(instance.object).json()['name']
        except:
            where = "Endroit inconnu"

        if who == where:
            where = "t'a envoyé un message privé"
        else:
            where = "t'a mentionné sur " + where

        html_message = loader.render_to_string(
            'email.html',
            {
                'on': (settings.INSTANCE_DEFAULT_CLIENT or settings.JABBER_DEFAULT_HOST),
                'instance': instance,
                'author': who,
                'object': where
            }
        )

        send_mail(
            'Notification sur ' + (settings.INSTANCE_DEFAULT_CLIENT or settings.JABBER_DEFAULT_HOST),
            instance.summary,
            settings.EMAIL_HOST_USER or "noreply@" + settings.JABBER_DEFAULT_HOST,
            [instance.user.email],
            fail_silently=True,
            html_message=html_message
        )
