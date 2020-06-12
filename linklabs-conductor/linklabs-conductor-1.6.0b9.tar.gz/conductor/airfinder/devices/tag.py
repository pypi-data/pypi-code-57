import logging

from conductor.airfinder.devices.node import Node
from conductor.airfinder.base import DownlinkMessageSpec
from conductor.util import Version

LOG = logging.getLogger(__name__)


class TagDownlinkMessageSpecV1_2(DownlinkMessageSpec):
    """ Message Spec for the Alert Tag v1.2.0. """
    header = {
        'def': ['msg_type', 'msg_spec_version'],
        'struct': '>BB',
        'defaults': [0x00, 0x01]
    }

    msg_types = {
        'Configuration': {
            'def': ['mask', 'heartbeat', 'loc_upd', 'scans_per_fix', 'net_lost_time', 'net_scan_int'],
            'struct': '>BHHBHH',
            'defaults': [0x00, 0x0258, 0x1e, 0x0f, 0x03, 0x012c, 0x03, 0x03, 0x01]
        },
        'DiagnosticMode': {
            'def': ['new_diag_mode'],
            'struct': '>B',
            'defaults': [0x0]
        },
    }


class TagDownlinkMessageSpecV1_3(TagDownlinkMessageSpecV1_2):
    """ Message Spec for the Alert Tag v1.3.0. """

    def __init__(self):
        super().__init__()
        # Update Message Spec Version.
        self.header.update({'defaults': [0x00, 0x02]})

        # - Added Accelerometer Configuration Message
        # - Added BLE Stat Reset Message.
        self.msg_types.update({
            "AccelerometerConfiguration": {
                'def': ['mask', 'accel_en', 'motion_thresh', 'motion_dur'],
                'struct': '>BBHH',
                'defaults': [0x00, 0x01, 30, 3]
            },
            "BleStatReset": {'type': 4}}
        )


class TagDownlinkMessageSpecV1_4(TagDownlinkMessageSpecV1_3):
    """ Message Spec for the Alert Tag v1.4.0. """

    def __init__(self):
        super().__init__()
        # Update Message Spec Version.
        self.header.update({'defaults': [0x00, 0x03]})

        # Update Configuration Message.
        #   - Add Mobile Mode Heartbeat.
        #   - Add Max SymBLE Retries.
        self.msg_types["Configuration"].update({
            'def': ['mask', 'heartbeat', 'loc_upd', 'scans_per_fix', 'net_lost_time', 'net_scan_int', 'mobile_hb',
                    'max_symble_retries'],
            'struct': '>BHHBHHHB',
            'defaults': [0x00, 0x0258, 0x1e, 0x0f, 0x03, 0x012c, 0x03, 0x03, 0x01, 900, 3]
        })

        # Added Reset Message
        self.msg_types.update({
            "Reset": {
                'type': 5,
                'def': ['reset_code'],
                'struct': '>I',
                'defaults': [0xd5837ed6]
            }
        })


class TagDownlinkMessageSpecV2_0(TagDownlinkMessageSpecV1_4):
    """ Message Spec for the Alert Tag v2.0.0. """

    def __init__(self):
        super().__init__()
        # Update Message Spec Version.
        self.header.update({'defaults': [0x00, 0x04]})

        # Update Configuration Message.
        #   - Add Mobile Mode Heartbeat.
        #   - Add Max SymBLE Retries.
        self.msg_types["Configuration"].update({
            'def': ['mask', 'profile0', 'profile1', 'profile2', 'profile3', 'profile4', 'max_symble_retries'],
            'struct': '>B26s26s26s26s26sB',
            'defaults': [0x00, bytearray(b'\xff' * 26),  bytearray(b'\xff' * 26), bytearray(b'\xff' * 26),
                         bytearray(b'\xff' * 26), bytearray(b'\xff' * 26), 3]
        })

        # Added Param Message
        self.msg_types.update(dict(ParamRequest={'type': 6}))


class Tag(Node):
    """ Represents a SymBLE Tag. C7 and E7 Hardware platforms. """
    application = "9f333a1ade8500df888f"

    @property
    def version(self):
        number = self._md.get("msgSpecVersion")
        if number == 1:
            return Version(1, 2, 0)
        elif number == 2:
            return Version(1, 3, 0)
        elif number == 3:
            return Version(1, 4, 0)
        elif number == 4:
            return Version(2, 0, 0)
        else:
            return Exception("Unsupported version!")

    @classmethod
    def _get_spec(cls, vers):
        if vers == Version(1, 2, 0):
            return TagDownlinkMessageSpecV1_2()
        elif vers == Version(1, 3, 0):
            return TagDownlinkMessageSpecV1_3()
        elif vers == Version(1, 4, 0):
            return TagDownlinkMessageSpecV1_4()
        elif vers == Version(2, 0, 0):
            return TagDownlinkMessageSpecV2_0()
        else:
            raise Exception("Unsupported message spec!")


class NordicThingy(Tag):
    """ Represents the Nordic Thingy Test Tag. """
    application = "6c030f3dcaf3055b1098"

    @classmethod
    def _get_spec(cls, vers):
        raise NotImplementedError


class S1Tag(Tag):
    """ Represents the legacy S1 Tag. """
    application = "4068973f7f00791a61f0"

    @classmethod
    def _get_spec(cls, vers):
        raise NotImplementedError


class S1TagGen2(S1Tag):
    """ S1 Tag with temperature """
    application = "150285a4e29b7856c7cc"

    @classmethod
    def _get_spec(cls, vers):
        raise NotImplementedError


class TestTag(Tag):
    """ Development and Testing Tag. """
    application = "9a6d019a9385b231f658"

    @classmethod
    def _get_spec(cls, vers):
        raise NotImplementedError
