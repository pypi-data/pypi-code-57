from abc import ABC
from typing import Any

from aistac.components.abstract_component import AbstractComponent

__author__ = 'Darryl Oatridge'

from aistac.properties.ledger_property_manager import LedgerPropertyManager


class AbstractLedger(AbstractComponent, ABC):

    @classmethod
    def from_env(cls, task_name: str=None, default_save=None, reset_templates: bool=None, align_connectors: bool=None,
                 default_save_intent: bool=None, default_intent_level: bool=None,  order_next_available: bool=None,
                 default_replace_intent: bool=None, **kwargs):
        """ Class Factory Method that builds the connector handlers taking the property contract path from
        the os.environ['HADRON_PM_PATH'] or, if not found, uses the system default,
                    for Linux and IOS '/tmp/components/contracts
                    for Windows 'os.environ['AppData']\\components\\contracts'
        The following environment variables can be set:
        'HADRON_PM_PATH': the property contract path, if not found, uses the system default
        'HADRON_PM_TYPE': a file type for the property manager. If not found sets as 'pickle'
        'HADRON_PM_MODULE': a default module package, if not set uses component default
        'HADRON_PM_HANDLER': a default handler. if not set uses component default

        This method calls to the Factory Method 'from_uri(...)' returning the initialised class instance

         :param task_name: The reference name that uniquely identifies a task or subset of the property manager
         :param default_save: (optional) if the configuration should be persisted
         :param reset_templates: (optional) reset connector templates from environ variables. Default True
                                (see `report_environ()`)
         :param align_connectors: (optional) resets aligned connectors to the template. default Default True
         :param default_save_intent: (optional) The default action for saving intent in the property manager
         :param default_intent_level: (optional) the default level intent should be saved at
         :param order_next_available: (optional) if the default behaviour for the order should be next available order
         :param default_replace_intent: (optional) the default replace existing intent behaviour
         :param kwargs: to pass to the property ConnectorContract as its kwargs
         :return: the initialised class instance
         """
        task_name = task_name if isinstance(task_name, str) else 'base'
        return super().from_env(task_name=task_name, default_save=default_save, reset_templates=reset_templates,
                                align_connectors=align_connectors, default_save_intent=default_save_intent,
                                default_intent_level=default_intent_level, order_next_available=order_next_available,
                                default_replace_intent=default_replace_intent)

    @property
    def pm(self) -> LedgerPropertyManager:
        """The properties manager instance"""
        return self._component_pm

    @property
    def ledger_catalog(self) -> dict:
        """returns a dictionary of managers and their tasks"""
        return self.pm.ledger_catalog

    def add_ledger(self, property_manager: Any, save: bool=None):
        """ adds a pm to the ledger

        :param property_manager: the instance of the property manager to add
        :param save: (optional) override of the default save action set at initialisation.
       """
        save = save if isinstance(save, bool) else self._default_save
        self.pm.set_ledger(property_manager)
        self.pm_persist(save)

    def remove_ledger_pm(self, manager: str, task: str, save: bool=None):
        """ removes a pm from the ledger

        :param manager: The name of the component manager
        :param task: The name of the manager task
        :param save: (optional) override of the default save action set at initialisation.
        :return True if removed, False if not
        """
        save = save if isinstance(save, bool) else self._default_save
        result = self.pm.remove_ledger(manager=manager, task=task)
        self.pm_persist(save)
        return result


