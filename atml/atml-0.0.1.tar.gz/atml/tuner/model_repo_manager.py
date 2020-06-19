import importlib
import os

from logzero import logger

from ..util import atm_util as util


class TunerModelManager(object):
    def __init__(self, run_id, dao, with_default):
        self.run_id = run_id
        self.dao = dao
        self.repo = {}
        self.count_map = {}

        logger.info('with_default: {0}'.format(with_default))
        if with_default:
            default_config = util.parse_model_space_yaml(os.path.join(os.path.dirname(__file__), 'config', 'default_models.yml'))
            for key in default_config:
                instance = self._get_instance_by_name(key)
                self.register(instance, default_config[key])

    def register(self, instance, search_space):
        module, clazz, full_name = util.class_detail(instance)
        if full_name in self.repo:
            logger.warning('{0} already in the repository'.format(full_name))
        else:
            search_space_dict = {}
            count = 1
            dist = False
            for item in search_space:
                prop_key = item['property']
                search_space_dict[prop_key] = {'_type': item['type'], '_value': item['value']}
                count *= len(item['value'])
                if item['type'] != 'choice':
                    dist = True
            if dist:
                count = 99999

            self.repo[full_name] = search_space_dict
            self.count_map[full_name] = str(count)

            self.dao.insert_search_space(self.run_id, full_name, instance, search_space_dict)  

    def _get_instance_by_name(self, full_name):
        dot_ind = full_name.rfind('.')
        module, clazz = full_name[:dot_ind], full_name[dot_ind+1:]
        instance = self._get_instance(module, clazz)
        return instance


    def _get_instance(self, module_name, class_name):
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        return class_()

