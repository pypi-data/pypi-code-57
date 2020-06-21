"""
Constants for authorization mocking
"""

MOCK_ACCOUNT_ID = "81a6dd2d-160e-4530-864d-e7ab524462a0"

MOCK_TOKEN = ("Bearer eyJraWQiOiIzUlRMQ1l1MFJWZ09LMlZSWWZ1S1dSVnE2WWhQa2JMT3BHM2o2ejArRDhJPSIsImFsZyI6IlJTMjU2In0."
              "eyJhdF9oYXNoIjoiZm5WdnRKYkpXdFJWRnhiSWVkNVU3USIsInN1YiI6IjgxYTZkZDJkLTE2MGUtNDUzMC04NjRkLWQ3YWI1MjQ0Nj"
              "JhMCIsImNvZ25pdG86Z3JvdXBzIjpbInVzLXdlc3QtMl9STm9kVGt1TkNfRmFjZWJvb2siXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ2"
              "5pdG8taWRwLnVzLXdlc3QtMi5hbWF6b25hd3MuY29tXC91cy13ZXN0LTJfUk5vZFRrdU5DIiwiY29nbml0bzp1c2VybmFtZSI6"
              "IkZhY2Vib29rXzI2NTI4MTQ1MDk4MzAzMSIsImdpdmVuX25hbWUiOiJNaXNoZWwiLCJhdWQiOiI2MzFuY2pibmVsazg1NGtv"
              "amphcGo1NTN0aCIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6IjI2NTI4MTQ1MDk4MzAzMSIsInByb3ZpZGVyTmFtZSI6IkZh"
              "Y2Vib29rIiwicHJvdmlkZXJUeXBlIjoiRmFjZWJvb2siLCJpc3N1ZXIiOm51bGwsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUN"
              "yZWF0ZWQiOiIxNTM2MzIwMDM1MTI3In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTUzODU1NDc2MywibmFtZSI6"
              "Ik1pc2hlbCBDcnVpc2UiLCJleHAiOjE1Mzg1NTgzNjMsImlhdCI6MTUzODU1NDc2MywiZmFtaWx5X25hbWUiOiJDcnVpc2UiLC"
              "JlbWFpbCI6InRlc3R1c2VyOTUxYmJAZ21haWwuY29tIn0.YMxi4xXdHgWikWHNPh-sr-gFNGTMlva4VJWCagGrIone6YTVX4uR"
              "gHK-du06nJ-bqqaZBTzZOwaV2NFp9oQDOI5TzMykYBskAEJ0CiI1YP_nUq8KcZRtElWPk6IbGtHhG2GqYxHedvCZxwKalWxi01"
              "iGnAayNbNA9-NaqPoXu_9J2VKC24lgbR7JEifwKBHzq37SmV20kyKeMVEzN7XxyQgoyUGr2ndfn3XT289_9MpaUNaaq66QxGMB"
              "UIC8jkqFGauZc7iCVxLuV79EFIX_Y4nGh95qNhBc8hQb4_TNhpSN2rnqk_ePypBcL54S26bWJgBxGr8bebDFM9q5OttjDg")

STANDARD_AUTHORIZER_CONTEXT = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "at_hash": "gnVvtJbJWtRVFxbIed3U7Q",
                "aud": "731ncjbnelk854kijjapj553th",
                "auth_time": "1538554763", "cognito:groups":
                "us-west-2_RNodTkuNC_Facebook",
                "cognito:username": "Facebook_9876543210",
                "email": "testuser123456@gmail.com",
                "exp": "Wed Oct 03 09:19:23 UTC 2018",
                "family_name": "User",
                "given_name": "Test",
                "iat": "Wed Oct 03 08:19:23 UTC 2018",
                "identities": ("{\"dateCreated\":\"1536320035127\",\"userId\":\"265281450983031\","
                               " \"providerName\":""\"Facebook\",\"providerType\":\"Facebook\","
                               " \"issuer\":null,\"primary\":\"true\"}"),
                "iss": "https://cognito-idp.us-west-2.amazonaws.com/us-west-2_WAVELENGTH_ACCOUNT",
                "name": "Test User",
                "sub": MOCK_ACCOUNT_ID,
                "token_use": "id"
            }
        }
    }
}
