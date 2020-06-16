from time import sleep

from test.DriverFactory import DriverFactory


class TestPageTitle(DriverFactory):
    def test_page_title_4(self):
        sleep(3)
        self.driver.find_element_by_id("classic_bottom_navigation_icon").click()
        assert self.driver.find_element_by_id("headerTxt").text == "Search Flights"

    def test_page_title_5(self):
        sleep(3)
        self.driver.find_element_by_id("classic_bottom_navigation_icon").click()
        assert self.driver.find_element_by_id("headerTxt").text == "Search Flights"

    def test_page_title_6(self):
        sleep(3)
        self.driver.find_element_by_id("classic_bottom_navigation_icon").click()
        assert self.driver.find_element_by_id("headerTxt").text == "Search Flights"
