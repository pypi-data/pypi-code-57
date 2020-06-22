# -*- coding: utf-8 -*-
from collective.z3cform.select2.widget.widget import MultiSelect2FieldWidget
from ideabox.policy import _
from ideabox.policy.content.project import IProject
from ideabox.policy.content.project import Project
from ideabox.policy.content.project import ProjectView
from plone import api
from plone.app.textfield.value import IRichTextValue
from plone.autoform import directives as form
from plone.indexer.decorator import indexer
from Products.CMFPlone.utils import getToolByName
from zope import schema
from zope.interface import implementer


class IPriorityAction(IProject):
    """IPriorityActionIProject"""

    form.widget(project_district=MultiSelect2FieldWidget)
    form.order_after(project_district='project_theme')
    project_district = schema.List(
        title=_(u"District(s) concerned"),
        value_type=schema.Choice(
            title=_(u"District(s) concerned"),
            vocabulary=u"collective.taxonomy.district",
        ),
        required=False,
    )

    strategic_objectives = schema.TextLine(
        title=_(u"Strategic Objectives"), required=False
    )

    operational_objectives = schema.TextLine(
        title=_(u"Operational objectives"), required=False
    )


@implementer(IPriorityAction)
class PriorityAction(Project):
    pass


class PriorityActionView(ProjectView):
    def get_state_progress(self):
        return api.content.find(
            context=self.context, portal_type="state_progress", sort_on="state_date"
        )[:4]


@indexer(IPriorityAction)
def searchabletext_priority_action(object, **kw):
    result = []

    fields = ["title", "description", "body", "original_author"]
    for field_name in fields:
        value = getattr(object, field_name, None)
        if IRichTextValue.providedBy(value):
            transforms = getToolByName(object, "portal_transforms")
            text = (
                transforms.convertTo("text/plain", value.raw, mimetype=value.mimeType)
                .getData()
                .strip()
            )
            result.append(text)
        else:
            text = value
            if text:
                result.append(text)
    return " ".join(result)
