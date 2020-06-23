"""
    Maintenance manager module
"""
from datetime import datetime
from sdc_helpers.models.client import Client
import boto3
from sdc_engine_helpers.date_utils import DateUtils
from sdc_engine_helpers.personalize.maintenance.campaign_state_manager import CampaignStateManager
from sdc_engine_helpers.personalize.maintenance.solution_state_manager import SolutionStateManager
from sdc_engine_helpers.personalize.manager import Manager


class MaintenanceManager(Manager):
    """
        Manage AWS Personalize solutions and campaigns
    """
    date_utils = None
    lambda_client = None
    personalize = None
    solution_state_manager = None
    campaign_state_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_utils = DateUtils()
        self.solution_state_manager = SolutionStateManager()
        self.campaign_state_manager = CampaignStateManager()
        self.personalize = boto3.client('personalize')

    def perform_maintenance(self):
        """
            Create new Personalize solution versions and update Personalize campaigns
            when required
        """
        # Get all active client subscriptions for the supplied service
        for client in self.query_helper.get_clients():
            # Set up a flag to decide whether its necessary to update this subscription
            # after maintenance of this subscription
            update = False

            subscription = self.query_helper.get_subscription(
                client_id=client.id,
                service_id=self.service.id,
                from_cache=False
            )

            solutions, engine_index = self.query_helper.get_engine_entity(
                client_id=client.id,
                service_id=self.service.id,
                engine_slug=self.engine_slug,
                entity_key='solutions',
                from_cache=False
            )

            if solutions is not None:
                response = self.perform_solution_maintenance(
                    client=client,
                    solutions=solutions
                )

                if response.get('solutions_updated') is True:
                    self.query_helper.update_solutions(
                        subscription=subscription,
                        engine_index=engine_index,
                        value=response.get('solutions')
                    )
                    update = True

            campaigns, engine_index = self.query_helper.get_engine_entity(
                client_id=client.id,
                service_id=self.service.id,
                engine_slug=self.engine_slug,
                entity_key='campaigns',
                from_cache=False
            )

            if campaigns is not None:
                response = self.perform_campaign_maintenance(
                    client=client,
                    campaigns=campaigns
                )

                if response.get('campaigns_updated') is True:
                    self.query_helper.update_campaigns(
                        subscription=subscription,
                        engine_index=engine_index,
                        value=response.get('campaigns')
                    )
                    update = True

            if update:
                self.query_helper.update_subscription(subscription=subscription)
                self.query_helper.flush_subscription_properties_cache(subscription=subscription)

    def perform_solution_maintenance(self, *, client: Client, solutions: list) -> dict:
        """
            Perform the required maintenance on a list of solutions

            args:
                client (Client): The client this maintenance is being performed for
                solutions (list): A list of solutions from the database to perform maintenance on

            returns:
                result (dict): A dictionary with an updated flag and resultant solutions

        """
        # Set up a flag to return if the solutions have been updated
        solutions_updated = False

        for index, solution in enumerate(solutions):
            # The solution arn is required to continue maintenance for this solution
            arn = solution.get('arn', None)

            if arn is None:
                continue

            state = self.solution_state_manager.get_state(
                solution=solution
            )

            if state.get('should_create_version') is True:
                print(
                    'Building solution version for client: {client_name}'
                    .format(client_name=client.name)
                )

                response = self.personalize.create_solution_version(
                    solutionArn=arn
                )

                print(
                    'Successfully started creation of solution version: {solution_version_arn}'
                    .format(solution_version_arn=response.get('solutionVersionArn'))
                )

                solutions[index]['version_status'] = 'CREATE IN_PROGRESS'
                solutions[index]['version_last_created_at'] = datetime.strftime(
                    datetime.now(),
                    self.date_utils.get_mysql_date_format()
                )

                next_version_creation_time = state.get('next_version_creation_time', None)
                if next_version_creation_time:
                    solutions[index]['next_version_creation_time'] = next_version_creation_time

                solutions_updated = True
            elif state.get('should_refresh_version_status') is True:
                new_version_status = state.get('new_version_status')

                print(
                    'Refreshing version status on solution: {arn} for client: {client_name}'
                    ' to {status}'
                    .format(
                        arn=arn,
                        client_name=client.name,
                        status=new_version_status
                    )
                )

                solutions[index]['version_status'] = new_version_status
                solutions_updated = True

        return {
            'solutions_updated': solutions_updated,
            'solutions': solutions
        }

    def perform_campaign_maintenance(self, *, client: Client, campaigns: list) -> dict:
        """
            Perform the required maintenance on a list of campaigns

            args:
                client (Client): The client this maintenance is being performed for
                campaigns (list): A list of campaigns from the database to perform maintenance on

            returns:
                result (dict): Dictionary containing:
                               1) campaigns_updated
                               2) Resultant campaigns list

        """
        # Set up a flag to return if the campaigns have been updated
        campaigns_updated = False

        # Some clients share the same campaigns so we return all refreshed defaults results
        # in a dictionary keyed by client and campaign arn. These can be used to replicate to
        # other clients campaigns in the database

        for index, campaign in enumerate(campaigns):
            # The campaign arn is required to continue maintenance for this campaign
            arn = campaign.get('arn', None)

            if arn is None:
                continue

            state = self.campaign_state_manager.get_state(
                campaign=campaign
            )

            if state.get('should_update') is True:
                latest_solution_version_arn = state.get(
                    'latest_solution_version_arn'
                )
                print(
                    'Updating campaign for client: {client_name} to solution version: {arn}'
                    .format(
                        client_name=client.name,
                        arn=latest_solution_version_arn
                    )
                )

                self.personalize.update_campaign(
                    campaignArn=arn,
                    solutionVersionArn=latest_solution_version_arn
                )

                print('Successfully started updating campaign: {arn}'.format(arn=arn))

                campaigns[index]['last_updated_at'] = datetime.strftime(
                    datetime.now(),
                    self.date_utils.get_mysql_date_format()
                )
                campaigns[index]['status'] = 'CREATE IN_PROGRESS'

                next_update_time = state.get('next_update_time', None)
                if next_update_time is not None:
                    campaigns[index]['next_update_time'] = next_update_time

                campaigns_updated = True
            elif state.get('should_refresh_status') is True:
                new_status = state.get('new_status')

                print(
                    'Refreshing status on campaign: {arn} for client: {client_name} to {status}'
                    .format(
                        arn=arn,
                        client_name=client.name,
                        status=new_status
                    )
                )

                campaigns[index]['status'] = new_status

                if state.get('refresh_default_results') is True:
                    default_results = state.get('new_default_results', None)
                    if default_results is not None:
                        print(
                            'Refreshing default results on campaign: {arn} '
                            'for client: {client_name}'
                            .format(
                                arn=arn,
                                client_name=client.name
                            )
                        )

                        campaigns[index]['default_results'] = default_results

                campaigns_updated = True

        return {
            'campaigns_updated': campaigns_updated,
            'campaigns': campaigns
        }
