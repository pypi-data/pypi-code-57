""" Test UNI filters """


import unittest
from ...libs.models.evc import EthernetVirtualCircuit
from ...libs.models.uni import UNI
from ...libs.core.evc_list import EvcsList


def create_uni(device, interface, tag_value):
    """ Create an UNI"""
    uni = UNI()
    uni.device = device
    uni.interface_name = interface
    uni.interface_description = interface
    uni.tag.type = 'vlan'
    uni.tag.value = tag_value
    return uni


def create_unis(uni_list):
    """ Create UNIs using tuples provided"""
    unis = list()
    for uni in uni_list:
        unis.append(create_uni(uni[0], uni[1], uni[2]))
    return unis


def filter_uni(evcs, device, interface, tag_value):
    """ filter per uni """
    evcs_names = list()
    for evc in evcs:
        for uni in evc.unis:
            if EvcsList().filter_uni(uni, device, interface, tag_value):
                evcs_names.append(evc.name)
                break

    return evcs_names


class TestFilterUnis(unittest.TestCase):
    """  Test filters of UNI """

    def setUp(self):
        """ Set Up Testing environment. Creates three EVCs with UNIs only. """
        self.evc_1 = EthernetVirtualCircuit()
        self.evc_1.name = "evc_1"
        self.evc_1.unis = create_unis([("device_a", "interface_a", 10),
                                       ("device_b", "interface_b", 10)])

        self.evc_2 = EthernetVirtualCircuit()
        self.evc_2.name = "evc_2"
        self.evc_2.unis = create_unis([("device_a", "interface_a", 20),
                                       ("device_c", "interface_c", 20)])

        self.evc_3 = EthernetVirtualCircuit()
        self.evc_3.name = "evc_3"
        self.evc_3.unis = create_unis([("device_a", "interface_b", 20),
                                       ("device_b", "interface_c", 20)])

        self.evcs = [self.evc_1, self.evc_2, self.evc_3]

        self.evcs_list = EvcsList()

    def test_filter_uni_no_filter_provided_assert_true(self):
        """ If no filters are request by user, all UNIs are good.
         Expected number of EVCs: 3 """
        evcs_names = filter_uni(self.evcs, device=False, interface=False,
                                tag_value=False)
        self.assertTrue(len(evcs_names) == 3)

    def test_filter_uni_only_device_provided_device_c_evc_2(self):
        """ Search for device_c. Only evc_2 should be listed. """
        evcs_names = filter_uni(self.evcs, device="device_c", interface=False,
                                tag_value=False)

        self.assertTrue(len(evcs_names) == 1)
        self.assertEqual(evcs_names[0], "evc_2")

    def test_filter_uni_only_device_provided_device_b_evc_1_evc_3(self):
        """ Search for device_b. evc_1 and evc_3 should be listed. """
        evcs_names = filter_uni(self.evcs, device="device_b", interface=False,
                                tag_value=False)

        self.assertTrue(len(evcs_names) == 2)
        self.assertEqual(evcs_names[0], "evc_1")
        self.assertEqual(evcs_names[1], "evc_3")

    def test_filter_uni_only_device_provided_device_d_no_evc(self):
        """ Search for device_d. No evc should be listed. """
        evcs_names = filter_uni(self.evcs, device="device_d", interface=False,
                                tag_value=False)

        self.assertTrue(len(evcs_names) == 0)

    def test_filter_uni_only_device_provided_device_a_all_evcs(self):
        """ Search for device_a. All evcs should be listed. """
        evcs_names = filter_uni(self.evcs, device="device_a", interface=False,
                                tag_value=False)

        self.assertTrue(len(evcs_names) == 3)
        self.assertEqual(evcs_names[0], "evc_1")
        self.assertEqual(evcs_names[1], "evc_2")
        self.assertEqual(evcs_names[2], "evc_3")

    def test_filter_device_a_interface_a_evc_1_evc_2(self):
        """ Search for device_a and interface_a. Evc_1 and evc_2 should be listed. """
        evcs_names = filter_uni(self.evcs, device="device_a", interface="interface_a",
                                tag_value=False)

        self.assertTrue(len(evcs_names) == 2)
        self.assertEqual(evcs_names[0], "evc_1")
        self.assertEqual(evcs_names[1], "evc_2")

    def test_filter_device_a_interface_b_evc_3(self):
        """ Search for device_a and interface_b. Only Evc_3 should be listed. """
        evcs_names = filter_uni(self.evcs, device="device_a", interface="interface_b",
                                tag_value=False)

        self.assertTrue(len(evcs_names) == 1)
        self.assertEqual(evcs_names[0], "evc_3")

    def test_filter_interface_b_evc_1_evc_3(self):
        """ Search for interface_b. Evc 1 and Evc_3 should be listed. """
        evcs_names = filter_uni(self.evcs, device=False, interface="interface_b",
                                tag_value=False)

        self.assertTrue(len(evcs_names) == 2)
        self.assertEqual(evcs_names[0], "evc_1")
        self.assertEqual(evcs_names[1], "evc_3")

    def test_filter_tag_value_20_evc_2_evc_3(self):
        """ Search for tag_value 20. Evc 2 and Evc_3 should be listed. """
        evcs_names = filter_uni(self.evcs, device=False, interface=False,
                                tag_value=20)

        self.assertTrue(len(evcs_names) == 2)
        self.assertEqual(evcs_names[0], "evc_2")
        self.assertEqual(evcs_names[1], "evc_3")

    def test_filter_tag_value_10_evc_1(self):
        """ Search for tag_value 10. Evc 1 should be listed. """
        evcs_names = filter_uni(self.evcs, device=False, interface=False,
                                tag_value=10)

        self.assertTrue(len(evcs_names) == 1)
        self.assertEqual(evcs_names[0], "evc_1")

    def test_filter_interface_b_tag_value_20_evc_3(self):
        """ Search for interface_b and tag_value 20.  Evc_3 should be listed. """
        evcs_names = filter_uni(self.evcs, device=False, interface="interface_b",
                                tag_value=20)

        self.assertTrue(len(evcs_names) == 1)
        self.assertEqual(evcs_names[0], "evc_3")

    def test_filter_device_a_tag_value_20_evc_2_evc_3(self):
        """ Search for device_a and tag_value 20. Evc 2 and Evc_3 should be listed. """
        evcs_names = filter_uni(self.evcs, device="device_a", interface=False,
                                tag_value=20)

        self.assertTrue(len(evcs_names) == 2)
        self.assertEqual(evcs_names[0], "evc_2")
        self.assertEqual(evcs_names[1], "evc_3")

    def test_filter_device_a_interface_a_tag_value_10_evc_1(self):
        """ Search for device_a, interface_a and tag_value 10. Evc 1 should be listed. """
        evcs_names = filter_uni(self.evcs, device="device_a", interface="interface_a",
                                tag_value=10)

        self.assertTrue(len(evcs_names) == 1)
        self.assertEqual(evcs_names[0], "evc_1")

    def test_filter_device_a_interface_a_tag_value_20_evc_2(self):
        """ Search for device_a, interface_a and tag_value 20. Evc 2 should be listed. """
        evcs_names = filter_uni(self.evcs, device="device_a", interface="interface_a",
                                tag_value=20)

        self.assertTrue(len(evcs_names) == 1)
        self.assertEqual(evcs_names[0], "evc_2")

    def test_filter_device_a_interface_a_tag_value_30_no_evc(self):
        """ Search for device_a, interface_a and tag_value 30. No evc should be listed. """
        evcs_names = filter_uni(self.evcs, device="device_a", interface="interface_a",
                                tag_value=30)

        self.assertTrue(len(evcs_names) == 0)


if __name__ == '__main__':
    unittest.main()
