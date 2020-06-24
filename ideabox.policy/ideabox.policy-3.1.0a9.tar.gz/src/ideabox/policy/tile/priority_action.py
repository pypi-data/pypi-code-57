# encoding: utf-8

from ideabox.policy import _
from plone import api
from plone.supermodel.model import Schema
from plone.tiles import Tile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema


class IPriorityActionTile(Schema):
    """A tile that displays a listing of content items"""

    title = schema.TextLine(
        title=_(u"Title"), required=True, default=_(u"Priority action")
    )


class LatestPriorityActionTile(Tile):
    template = ViewPageTemplateFile("templates/priority_action.pt")

    def __call__(self):
        return self.template()

    @property
    def title(self):
        return self.data.get("title") or _(u"Priority action")

    def lastcontent(self):
        return api.content.find(
            portal_type="priority_action", sort_on="created", sort_order="reverse"
        )[0]

    def contents(self):
        return api.content.find(
            portal_type="priority_action", sort_on="created", sort_order="reverse"
        )[1:6]

    def folder_projects(self):
        folder = api.content.find(portal_type="Folder", id="projets")
        if len(folder) == 1:
            return folder[0].getURL()
        return False

    @property
    def default_image(self):
        return "{0}/project_default.jpg".format(api.portal.get().absolute_url())
