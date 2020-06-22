from typing import Any

from aistac.handlers.abstract_handlers import ConnectorContract, HandlerFactory
from aistac.properties.abstract_properties import AbstractPropertyManager

__author__ = 'Darryl Oatridge'


class LedgerPropertyManager(AbstractPropertyManager):

    def __init__(self, task_name: str, username: str):
        """Abstract Class for the Master Properties"""
        root_keys = ['ledger']
        knowledge_keys = []
        super().__init__(task_name=task_name, root_keys=root_keys, knowledge_keys=knowledge_keys, username=username)

    @property
    def ledger_catalog(self) -> dict:
        """returns a dictionary of managers and their tasks"""
        rtn_dict = {}
        for manager in self.get(self.KEY.component_key, {}).keys():
            if manager not in rtn_dict:
                rtn_dict[manager] = []
            for task in self.get(self.join(self.KEY.component_key, manager), {}).keys():
                rtn_dict[manager].append(task)
        return rtn_dict

    def get_ledger(self, manager: str, task: str) -> dict:
        """returns the property manager

        :param manager:The name of the component manager
        :param task: The name of the manager task
        :return: a dictionary of properties
        """
        if self.is_key(self.join(self.KEY.component_key, manager, task)):
            uri = self.get(self.join(self.KEY.component_key, manager, task, 'raw_uri'))
            module = self.get(self.join(self.KEY.component_key, manager, task, 'raw_module_name'))
            handler = self.get(self.join(self.KEY.component_key, manager, task, 'raw_handler'))
            version = self.get(self.join(self.KEY.component_key, manager, task, 'raw_version'))
            kwargs = self.get(self.join(self.KEY.component_key, manager, task, 'raw_kwargs'))
            cc = ConnectorContract(uri=uri, module_name=module, handler=handler, version=version, **kwargs)
            cfg_dict = HandlerFactory.instantiate(cc).load_canonical()
            return cfg_dict.get(manager, {}).get(task, {})
        raise ValueError(f"Unable to find a manager '{manager}' with task '{task}' in the ledger")

    def has_ledger(self, manager: str, task: str=None) -> bool:
        """test if a manager or task has been registered

        :param manager: The name of the component manager
        :param task: (optional) The name of the manager task
        :return:
        """
        if isinstance(task, str):
            if self.is_key(self.join(self.KEY.component_key, manager, task)):
                return True
            return False
        if self.is_key(self.join(self.KEY.component_key, manager)):
            return True
        return False

    def set_ledger(self, property_manager: Any):
        """ sets the component properties from the property manager

        :param property_manager: the property manager of the component
        """
        if not isinstance(property_manager, AbstractPropertyManager):
            raise ValueError("The property_manager must be a concrete implementation of the AbstractPropertyManager")
        manager = property_manager.manager_name()
        task = property_manager.task_name
        connector_contract = property_manager.get_connector_contract(property_manager.CONNECTOR_PM_CONTRACT)
        base_key = self.join(self.KEY.component_key, manager, task,)
        self.set(self.join(base_key, 'raw_uri'), connector_contract.raw_uri)
        self.set(self.join(base_key, 'raw_module_name'), connector_contract.raw_module_name)
        self.set(self.join(base_key, 'raw_handler'), connector_contract.raw_handler)
        self.set(self.join(base_key, 'raw_version'), connector_contract.raw_version)
        self.set(self.join(base_key, 'raw_kwargs'), connector_contract.raw_kwargs)

    def reset_ledger(self):
        """resets the All ledger properties"""
        self._base_pm.remove(self.KEY.component_key)
        self.set(self.KEY.component_key, {})
        return

    def remove_ledger(self, manager: str, task: str):
        """ removes the ledger pm entry.

        :param manager: The name of the component manager
        :param task: The name of the manager task
        :return True if removed, False if not
        """
        if self.is_key(self.join(self.KEY.component_key, manager, task)):
            return self.remove(self.join(self.KEY.component_key, manager, task))
        return False
    
    def report_ledger(self, manager_filter: [str, list]=None) -> dict:
        """ generates a report on the source contract

        :param manager_filter: (optional) filters on the manager name.
        :return: dict
        """
        manager_filter = self.list_formatter(manager_filter)
        rtn_dict = {'manager_name': [], 'task_name': [], 'description': [], 'version': []}
        for manager in self.get(self.KEY.component_key, {}).keys():
            if isinstance(manager_filter, list) and manager_filter and manager not in manager_filter:
                continue
            for task in self.get(self.join(self.KEY.component_key, manager), {}).keys():
                rtn_dict['manager_name'].append(manager)
                rtn_dict['task_name'].append(task)
                ledger = self.get_ledger(manager=manager, task=task)
                rtn_dict['description'].append(ledger.get('description', ''))
                rtn_dict['version'].append(ledger.get('version', ''))
        return rtn_dict
