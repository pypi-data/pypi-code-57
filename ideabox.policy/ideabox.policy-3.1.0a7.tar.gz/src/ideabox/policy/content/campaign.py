# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class ICampaign(model.Schema):
    pass


@implementer(ICampaign)
class Campaign(Container):
    pass
