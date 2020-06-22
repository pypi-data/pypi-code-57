"""
    Solution state manager module
"""
from datetime import datetime
import sdc_helpers.utils as utils
import boto3
from sdc_engine_helpers.personalize.maintenance.date_utils import DateUtils


class SolutionStateManager:
    """
        Given a database solution object, check whether a new solution version needs to be
        created OR whether the status in the database needs to be refreshed
    """
    personalize = None
    date_utils = None

    def __init__(self):
        self.personalize = boto3.client('personalize')
        self.date_utils = DateUtils()

    def get_state(self, *, solution: dict) -> dict:
        """
            Get the current state of the solution in Personalize

            args:
                solution (dict): Solution from the database

            returns:
                state (dict): Dictionary containing:
                              1) should_create_version
                              2) should_refresh_version_status
                              3) next_version_creation_time (if frequency specified)
                              4) new_version_status

        """
        state = {
            'should_create_version': False,
            'should_refresh_version_status': False,
            'next_version_creation_time': None,
            'new_version_status': None
        }

        # Get Personalize solution from the Personalize client, an exception is thrown if
        # the solution arn is not found
        personalize_solution_response = self.personalize.describe_solution(
            solutionArn=solution.get('arn')
        )
        personalize_solution = personalize_solution_response.get('solution')

        # Check for creation
        state['should_create_version'] = self.should_create_solution_version(
            solution=solution,
            personalize_solution=personalize_solution
        )

        if state['should_create_version']:
            this_version_creation_time = solution.get('next_version_creation_time', None)
            version_creation_frequency = solution.get('version_creation_frequency', None)

            if version_creation_frequency:
                state['next_version_creation_time'] = self.date_utils.get_next_time(
                    this_time=this_version_creation_time,
                    frequency=version_creation_frequency
                )
        else:
            # Check if the database version status needs to be updated
            version_status = solution.get('version_status', None)
            personalize_solution_status = self.get_personalize_version_status(
                personalize_solution=personalize_solution
            )

            if personalize_solution_status != version_status:
                state['should_refresh_version_status'] = True
                state['new_version_status'] = personalize_solution_status

        return state

    @staticmethod
    def should_create_solution_version(*, solution: dict, personalize_solution: dict) -> bool:
        """
            Check whether a solution version should be created when all of the following are true:

            1) The latest solution version in Personalize is ACTIVE or FAILED
            2) The current time is >= the scheduled next version creation time (if specified)

            args:
                solution (dict): Solution from the database
                personalize_solution (dict): Solution from Personalize

            returns:
                result (bool): Should create solution version

        """
        # If the latest solution version is still creating in Personalize, don't create
        personalize_solution_version_status = utils.dict_query(
            dictionary=personalize_solution,
            path='latestSolutionVersion.status'
        )

        if personalize_solution_version_status not in ['ACTIVE', 'CREATE FAILED']:
            return False

        # If the Personalize solution version creation failed, create a new version immediately
        if personalize_solution_version_status == 'CREATE FAILED':
            return True

        version_creation_frequency = solution.get('version_creation_frequency', None)

        if version_creation_frequency:
            next_version_creation_time = solution.get('next_version_creation_time')
            if next_version_creation_time:
                if (
                        datetime.now() <
                        datetime.strptime(next_version_creation_time, "%Y-%m-%d %H:%M:%S")
                ):
                    return False

        return True

    @staticmethod
    def get_personalize_version_status(*, personalize_solution: dict) -> str:
        """
            Get Personalize solution version status

            args:
                personalize_solution (dict): Solution from Personalize

            returns:
                status (str): Personalize solution version status

        """

        return utils.dict_query(
            dictionary=personalize_solution,
            path='latestSolutionVersion.status'
        )
