import os

import rollbar

from testcase.app.drilling_efficiency_app import DrillingEfficiency

rollbar_token = os.getenv("ROLLBAR_TOKEN")
env = os.getenv("ENVIRONMENT", os.getenv("APP_ENV"))

if rollbar_token and env:
    rollbar.init(rollbar_token, env, handler='blocking')


@rollbar.lambda_function
def lambda_handler(event, context):
    """
    This function is the main entry point of the AWS Lambda function
    :param event: a scheduler or kafka event
    :param context: AWS Context
    :return:
    """
    app = DrillingEfficiency(rollbar=rollbar)
    app.load(event)
    app.run_modules()
    app.save_state()
