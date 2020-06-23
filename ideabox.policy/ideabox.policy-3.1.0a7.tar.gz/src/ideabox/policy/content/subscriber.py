# -*- coding: utf-8 -*-

from ideabox.policy.content.project import IProject
from ideabox.policy.utils import _activate_dashboard_navigation
from tempfile import mkstemp
from zope.globalrequest import getRequest
from plone.protect.auto import safeWrite

import os


def project_image_changed(obj, event):
    if hasattr(obj, "aq_parent") is False:
        return
    if IProject.providedBy(obj.aq_parent):
        obj.aq_parent.reindexObject(idxs=["project_picture"])


def project_added(obj, event):
    request = getRequest()
    safeWrite(obj, request)
    obj.allow_discussion = True


def campaign_added(obj, event):
    file = open(os.path.dirname(__file__) + "/../faceted/config/campaign.xml")
    xml = file.read()
    file.close()

    xml = xml.replace(
        '<property name="default">//REMPLACE//</property>',
        '<property name="default">{0}</property>'.format(
            "/{0}".format("/".join(obj.absolute_url_path().split("/")[2:]))
        ),
    )
    fd, path = mkstemp()
    with open(path, "w") as f:
        f.write(xml)
    os.close(fd)
    _activate_dashboard_navigation(obj, path)
    request = getRequest()
    request.response.redirect(obj.absolute_url())
