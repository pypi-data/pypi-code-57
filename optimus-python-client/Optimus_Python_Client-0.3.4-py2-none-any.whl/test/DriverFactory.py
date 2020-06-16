import pytest

from remote.OptimusCloudDriver import OptimusCloudDriver
from remote.OptimusCloudManager import OptimusCloudManager


class DriverFactory(object):
    @pytest.fixture(scope='function', autouse=True)
    def setUp(self) -> None:
        desired_caps = {
            'platformName': 'Android',
            'appPackage': 'com.cleartrip.android',
            'appActivity': 'com.cleartrip.android.activity.common.SplashActivity'
        }
        self.mobileDriverDetails = OptimusCloudDriver().createDriver(desiredCapabilities=desired_caps)
        self.driver = self.mobileDriverDetails.mobileDriver

    @pytest.fixture(scope='function', autouse=True)
    def tearDown(self) -> None:
        OptimusCloudManager().releaseSession(self.mobileDriverDetails)
