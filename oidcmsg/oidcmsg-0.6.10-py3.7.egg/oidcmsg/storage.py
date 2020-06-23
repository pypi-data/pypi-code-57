import copy

from abstorage.init import get_storage_class
from abstorage.init import get_storage_conf
from abstorage.init import init_storage
from cryptojwt import KeyJar
from cryptojwt.key_jar import init_key_jar


def add_issuer(conf, issuer):
    res = {}
    for key, val in conf.items():
        if key == 'abstract_storage_cls':
            res[key] = val
        else:
            _val = copy.deepcopy(val)
            _val['issuer'] = issuer
            res[key] = _val
    return res


class OidcEntity:
    def __init__(self, config=None, keyjar=None):
        db_conf = config.get('db_conf')
        if db_conf:
            db_conf = add_issuer(db_conf, config['issuer'])
            self.storage_cls = get_storage_class(db_conf)

        self.db = init_storage(db_conf)

        self.keyjar = self._keyjar(keyjar, db_conf, config)

    def add_boxes(self, boxes, db_conf):
        for attr, id in boxes.items():
            setattr(self, attr, init_storage(db_conf, id))

    def _keyjar(self, keyjar=None, db_conf=None, conf=None):
        if keyjar is None:
            if db_conf:
                if 'jwks' in conf:
                    args = {k: v for k, v in conf["jwks"].items() if k != "uri_path"}
                    return init_key_jar(storage_conf=db_conf.get('keyjar'), **args)
                else:
                    return KeyJar(abstract_storage_cls=self.storage_cls,
                                         storage_conf=get_storage_conf(db_conf, 'keyjar'))
            else:
                if 'jwks' in conf:
                    args = {k: v for k, v in conf["jwks"].items() if k != "uri_path"}
                    return init_key_jar(**args)
                else:
                    return KeyJar()
        else:
            return keyjar

    def set(self, item, value):
        self.db[item] = value

    def get(self, item):
        if item == 'seed':
            return bytes(self.db[item], 'utf-8')
        else:
            return self.db[item]
