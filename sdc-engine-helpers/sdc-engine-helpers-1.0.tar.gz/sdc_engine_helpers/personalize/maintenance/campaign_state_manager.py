"""
    Campaign state manager module
"""
from datetime import datetime
import sdc_helpers.utils as utils
import boto3
from sdc_engine_helpers.date_utils import DateUtils


class CampaignStateManager:
    """
        Given a database campaign object, check whether the Personalize campaign needs to be
        updated OR whether the status in the database needs to be refreshed. If so and the
        original status was CREATE IN_PROGRESS, we need to refresh the campaign's default
        results in the database
    """
    personalize = None
    personalize_runtime = None
    date_utils = None

    def __init__(self):
        self.personalize = boto3.client('personalize')
        self.personalize_runtime = boto3.client('personalize-runtime')
        self.date_utils = DateUtils()

    def get_state(self, *, campaign: dict) -> dict:
        """
            Get the current state of the campaign in Personalize

            args:
                campaign (dict): Campaign from the database

            returns:
                state (dict): Dictionary containing:
                              1) should_update flag
                              2) should_refresh_status
                              3) latest_solution_version_arn
                              4) next_update_time (if frequency specified)
                              5) new_status
                              6) refresh_default_results
                              7) new_default_results

        """
        # Get Personalize campaign from Personalize client, an exception is thrown if
        # the campaign arn is not found
        personalize_campaign_response = self.personalize.describe_campaign(
            campaignArn=campaign.get('arn')
        )
        personalize_campaign = personalize_campaign_response.get('campaign')

        state = {
            'should_update': False,
            'should_refresh_status': False,
            'latest_solution_version_arn': None,
            'next_update_time': None,
            'new_status': None,
            'refresh_default_results': False,
            'new_default_results': None
        }

        personalize_solution = self.get_solution(personalize_campaign=personalize_campaign)

        # Check for update
        state['should_update'] = self.should_update(
            campaign=campaign,
            personalize_campaign=personalize_campaign,
            personalize_solution=personalize_solution
        )

        if state['should_update']:
            state['latest_solution_version_arn'] = utils.dict_query(
                dictionary=personalize_solution,
                path='latestSolutionVersion.solutionVersionArn'
            )

            this_update_time = campaign.get('next_update_time', None)
            update_frequency = campaign.get('update_frequency', None)

            if update_frequency:
                state['next_update_time'] = self.date_utils.get_next_time(
                    this_time=this_update_time,
                    frequency=update_frequency
                )
        else:
            # Check if the database status needs to be updated
            status = campaign.get('status', None)
            personalize_status = self.get_personalize_status(
                personalize_campaign=personalize_campaign
            )

            if personalize_status != status:
                state['should_refresh_status'] = True
                state['new_status'] = personalize_status

                if status == 'CREATE IN_PROGRESS' and personalize_status == 'ACTIVE':
                    personalize_default_results = self.get_default_results(campaign=campaign)
                    default_results = campaign.get('default_results', [])
                    if default_results != personalize_default_results:
                        state['refresh_default_results'] = True
                        state['new_default_results'] = personalize_default_results

        return state

    def get_solution(self, *, personalize_campaign: dict) -> dict:
        """
            Obtain the latest solution version for the solution the campaign uses by:
                1) Describing the solution version the campaign is currently using
                2) Describing the solution for the above solution version

            args:
                personalize_campaign(dict): Campaign from Personalize

            returns:
                result (bool): The latest solution version for the campaign

        """
        personalize_solution_version_response = self.personalize.describe_solution_version(
            solutionVersionArn=personalize_campaign['solutionVersionArn']
        )

        personalize_solution_version = personalize_solution_version_response.get('solutionVersion')

        personalize_solution_response = self.personalize.describe_solution(
            solutionArn=personalize_solution_version['solutionArn']
        )

        return personalize_solution_response.get('solution')

    def should_update(
            self,
            *,
            campaign: dict,
            personalize_campaign: dict,
            personalize_solution: dict
    ) -> bool:
        """
            Check whether a campaign should be updated when all of the following are true

            1) The latest campaign update in Personalize is ACTIVE or FAILED
            2) The campaign isn't on the latest solution version
            3) The latest solution version is ACTIVE
            4) The current time is >= the scheduled next campaign update time (if specified)

            args:
                campaign (dict): Campaign from the database
                personalize_campaign(dict): Campaign from Personalize

            returns:
                result (bool): Should update campaign

        """
        # If the latest solution version is still creating in Personalize, don't update
        personalize_campaign_status = self.get_personalize_status(
            personalize_campaign=personalize_campaign
        )

        if personalize_campaign_status not in ['ACTIVE', 'CREATE FAILED']:
            return False

        # If the Personalize campaign update failed, update the campaign immediately
        if personalize_campaign_status == 'CREATE FAILED':
            return True

        latest_personalize_solution_version_arn = utils.dict_query(
            dictionary=personalize_solution,
            path='latestSolutionVersion.solutionVersionArn'
        )

        # Don't update campaign if its on the latest solution version
        if (
                personalize_campaign.get('solutionVersionArn') ==
                latest_personalize_solution_version_arn
        ):
            return False

        latest_personalize_solution_version_status = utils.dict_query(
            dictionary=personalize_solution,
            path='latestSolutionVersion.status'
        )

        # Don't update campaign if the latest solution version is not active
        if latest_personalize_solution_version_status != 'ACTIVE':
            return False

        next_update_time = campaign.get('next_update_time', None)
        update_frequency = campaign.get('update_frequency', None)

        if next_update_time and update_frequency:
            next_update_time = datetime.strptime(next_update_time, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()

            if now < next_update_time:
                return False

        return True

    @staticmethod
    def get_personalize_status(*, personalize_campaign: dict) -> str:
        """
            Get Personalize status

            args:
                personalize_campaign (dict): Campaign from Personalize

            returns:
                status (str): Personalize status

        """

        return utils.dict_query(
            dictionary=personalize_campaign,
            path='latestCampaignUpdate.status'
        )

    def get_default_results(self, *, campaign: dict) -> list:
        """
            Get Personalize campaign default results

            args:
                campaign (dict): Campaign from the database

            returns:
                default_results (list): Personalize campaign default results

        """
        results = []

        response = self.personalize_runtime.get_recommendations(
            campaignArn=campaign['arn'],
            itemId='notinmodel'
        )

        item_list = response.get('itemList', None)
        if item_list is not None:
            for item in item_list:
                item_id = item.get('itemId', None)
                if item_id is not None:
                    results.append(item_id)

        return results
