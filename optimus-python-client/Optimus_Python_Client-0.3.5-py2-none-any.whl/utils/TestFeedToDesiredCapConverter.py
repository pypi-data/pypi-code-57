from json.decoder import JSONObject

from utils.JsonUtil import JsonUtil


class TestFeedToDesiredCapConverter:
    appJson = JSONObject

    def __init__(self, testFeed):
        jsonUtil = JsonUtil
        self.appJson = jsonUtil.getAppJson(testFeed)

    # def convert(self):
    #     desiredCapabilitiesList = []
    #     testFeedArray = self.appJson.get("testFeed")
    #     for i in range(0, len(testFeedArray)):
    #         testFeedJSON = testFeedArray.get(i)
    #         print("Updated testFeed " + testFeedJSON)
    #         desiredCapabilities = CapabilitiesBuilder(testFeedJSON).buildCapabilities()
    #         desiredCapabilitiesList.append(desiredCapabilities)
    #     return desiredCapabilitiesList
