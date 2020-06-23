"""
   SDC subscription model module
"""
from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship, deferred, query_expression
from sdc_helpers.models.model import Model, models_namespace


class Subscription(Model):
    """
       SDC Subscription model class
    """
    # pylint: disable=too-few-public-methods
    __tablename__ = 'subscriptions'

    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id'), primary_key=True)
    # by default lazy load properties to avoid large data stores from automatically being pulled
    # at query time - use .options(undefer('properties')) on query to override default behaviour
    properties = deferred(Column(JSON))
    properties_node = query_expression()

    client = relationship(
        '{models_namespace}.client.Client'.format(
            models_namespace=models_namespace
        )
    )
    service = relationship(
        '{models_namespace}.service.Service'.format(
            models_namespace=models_namespace
        )
    )

    def __init__(self, **kwargs):
        """
            Creation of subscription model
        """
        super().__init__(**kwargs)
        self.client_id = kwargs.get('client_id')
        self.service_id = kwargs.get('service_id')
