"""
    Helpers module used by all engines
"""

def get_engine(*, properties: dict, slug: str, return_index: bool = False):
    """
        Get a specific engine from subscription properties

        args:
            properties (dict): Subscription properties for a client
            slug (str): The engine's slug
            return_index (bool): Return the index the engine was found in the properties

        returns:
            engine_dict (dict): The requested engine dictionary from the properties if found

    """
    engines = properties.get('engines', None)

    if engines is not None:
        for index, engine in enumerate(engines):
            if engine.get('slug') == slug:
                if return_index:
                    return engine, index

                return engine

    if return_index:
        return None, None

    return None


def get_dataset(*, engine: dict, label: str):
    """
        Get a specific dataset from an engine dictionary

        args:
            engine (dict): Subscription properties engine
            label (str): Label describing what the dataset is for

        returns:
            dataset_dict (dict): The requested dataset dictionary from the engine if found

    """
    datasets = engine.get('datasets', None)

    if datasets is not None:
        for dataset in datasets:
            if dataset.get('label') == label:
                return dataset

    return None

def get_campaign(engine: dict, **kwargs):
    """
        Get a specific campaign from an engine dictionary

        args:
            engine (dict): Subscription properties engine
            recipe (str): The recipe of the campaign e.g related_items
            event_type (str): Supplied if the campaign only involves certain events e.g
                              only listing views, but not listing enquiries

        returns:
            campaign_dict (dict): The requested campaign dictionary from the engine if found

    """
    arn = kwargs.get('arn', None)
    recipe = kwargs.get('recipe', None)
    event_type = kwargs.get('event_type', None)

    campaigns = engine.get('campaigns', None)

    if campaigns is not None:
        for campaign in campaigns:
            if (
                    (
                        arn is not None and campaign.get('arn') == arn
                    ) or
                    (
                        campaign.get('recipe') == recipe and
                        (event_type is None or campaign.get('event_type') == event_type)
                    )
            ):
                return campaign

    return None
