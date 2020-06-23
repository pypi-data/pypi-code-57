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


class OidcContext:
    def __init__(self, config=None, keyjar=None):
        self.db_conf = config.get('db_conf')
        if self.db_conf:
            self.db_conf = add_issuer(self.db_conf, config['issuer'])
            self.storage_cls = get_storage_class(self.db_conf)

        self.db = init_storage(self.db_conf)
        self.keyjar = self._keyjar(keyjar, self.db_conf, config)

    def add_boxes(self, boxes, db_conf):
        for key, attr in boxes.items():
            setattr(self, attr, init_storage(db_conf, key))

    def _keyjar(self, keyjar=None, db_conf=None, conf=None):
        if keyjar is None:
            if db_conf:
                if 'keydefs' in conf:
                    args = {k: v for k, v in conf["keydefs"].items() if k != "uri_path"}
                    return init_key_jar(abstract_storage_cls=self.storage_cls,
                                        storage_conf=get_storage_conf(db_conf, 'keyjar'), **args)
                else:
                    _keyjar = KeyJar(abstract_storage_cls=self.storage_cls,
                                     storage_conf=get_storage_conf(db_conf, 'keyjar'))
                    if 'jwks' in conf:
                        _keyjar.import_jwks(conf['jwks'], '')
                    return _keyjar
            else:
                if 'keydefs' in conf:
                    args = {k: v for k, v in conf["jwks"].items() if k != "uri_path"}
                    return init_key_jar(**args)
                else:
                    _keyjar = KeyJar()
                    if 'jwks' in conf:
                        _keyjar.import_jwks(conf['jwks'], '')
                    return _keyjar
        else:
            return keyjar

    def set(self, item, value):
        self.db[item] = value

    def get(self, item):
        if item == 'seed':
            return bytes(self.db[item], 'utf-8')
        else:
            return self.db[item]
