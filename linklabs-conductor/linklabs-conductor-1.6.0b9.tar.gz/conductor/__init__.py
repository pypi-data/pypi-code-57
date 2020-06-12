""" This module wraps the Conductor API. """
CONDUCTOR_LIBRARY_VERSION = '1.6.0b8'

PRODUCTION = 'conductor.link-labs'
DEVELOP = 'dev.link-labs'
HOSPITALITY = 'hospitality.airfinder'
UAT = 'hospitality-uat.airfinder'

INSTANCES = [PRODUCTION, DEVELOP, HOSPITALITY, UAT]

import conductor
from conductor.account import ConductorAccount
from conductor.asset_group import AssetGroup
from conductor.devices.gateway import Gateway
from conductor.devices.module import Module
from conductor.event_count import EventCount
from conductor.subject import ConductorSubject, UplinkSubject, DownlinkSubject
from conductor.subscriptions import ZeroMQSubscription
from conductor.tokens import AppToken, NetToken
import conductor.util
