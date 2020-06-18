"""Base no sql abstract class for nosqlmodels"""
import json
import os
import uuid
import zipfile
from typing import Dict, Any, List, Optional

# noinspection Mypy
from simplejsonobject import JsonObject  # noqa

from nosqlmodel.connectors.redisconnector import RedisConnector

__author__ = 'ozgur'
__creation_date__ = '12.09.2019' '13:48'


class BaseNoSqlModel(JsonObject):  # pylint: disable=too-many-public-methods
    """
    Nosql model with basic functionality\n
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta info"""
        connector = RedisConnector()
        indexkey = None

    def __init__(self):
        self.idkey = None

    def delete_table(self):
        """
        deletes table from db\n
        :return:
        """
        self.Meta.connector.delete_table()

    def create_table(self):
        """
        creates a new table, delete first if exists \n
        :return:
        """
        self.Meta.connector.create_table()

    @classmethod
    def flush(cls):
        """
        flushes al records\n
        :return: None
        """
        cls.Meta.connector.flush()

    @classmethod
    def dbsize(cls) -> int:
        """
        returns the itemcount in db\n
        :return: item count
        """
        return cls.Meta.connector.dbsize()

    @classmethod
    def get_keys(cls, pattern: str = "*") -> List[str]:
        """
        return all idkeys in db\n
        :return:
        """
        return cls.Meta.connector.keys(pattern)

    def get_by_id(self, idkey: str) -> bool:
        """
        get item by id\n
        :return:
        """
        retval = False
        ret = self.Meta.connector.get(idkey)
        if ret and isinstance(ret, dict):
            self.from_dict(ret)
            retval = True
        return retval

    def get_or_create_by_id(self, idkey: str) -> bool:
        """
        get item by id\n
        :return:
        """
        ret = self.Meta.connector.get(idkey)
        if ret and isinstance(ret, dict):
            self.from_dict(ret)
            retval = True
        else:
            if self.Meta.indexkey:
                self.__dict__[self.Meta.indexkey] = idkey
            else:
                raise KeyError("indexkey not defined")
            retval = False
        return retval

    @classmethod
    def get_multi(cls, keylist: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        get value by key\n
        :param keylist: list of strings
        :return: [objectdict]
        """
        return cls.Meta.connector.get_multi(keylist)

    @classmethod
    def get_all_as_list(cls) -> List[Optional[Dict[str, Any]]]:
        """
        returns all db as list of item dicts\n
        :return:  [object_dict]
        """
        return cls.Meta.connector.get_all_as_list()

    @classmethod
    def get_all_as_dict(cls) -> Dict[str, Optional[Dict[str, Any]]]:
        """
        returns all db as dict of item dicts\n
        :return:  {"id":object_dict,}
        """
        return cls.Meta.connector.get_all_as_dict()

    @classmethod
    def get_all_as_objectlist(cls) -> List['BaseNoSqlModel']:
        """
        returns all db as list of item objects\n
        :return:  [object]
        """
        retlist = []
        for itemdict in cls.get_all_as_list():
            if isinstance(itemdict, dict):
                retobj = cls()
                retobj.from_dict(itemdict)
                retlist.append(retobj)
        return retlist

    @classmethod
    def get_all_as_objectdict(cls) -> Dict[str, 'BaseNoSqlModel']:
        """
        returns all db as dict of item objects\n
        :return:  {key:object}
        """
        retdict = {}
        for key, itemdict in cls.get_all_as_dict().items():
            if isinstance(itemdict, dict):
                retobj = cls()
                retobj.from_dict(itemdict)
                retdict[key] = retobj
        return retdict

    def save_to_cache(self, tags: List[str] = None, compress=True) -> bool:
        """
        saves object\n

        :param tags: additional tags will added when saved
        :type compress: will save data compressed in db
        :return: success status
        """
        if not self.idkey:
            if self.Meta.indexkey:
                bnoid = self.__dict__.get(self.Meta.indexkey, None)
                self.idkey = str(bnoid) if bnoid else str(uuid.uuid4())
            else:
                self.idkey = str(uuid.uuid4())
        else:
            pass
        if compress:
            sdict = self.to_dict_compressed()
        else:
            sdict = self.to_dict()

        retval = self.Meta.connector.upsert(self.idkey, sdict)

        if tags:
            tnew = [x for x in tags if x]
            self.add_tags_to_item(tnew)

        return retval

    @classmethod
    def save_multi(cls, itemdict: Dict[str, Dict[str, Any]]):
        """
        saves multiple items at once\n
        :param itemdict: dict of objects dictionaries
        :return: None
        """
        cls.Meta.connector.upsert_multi(itemdict)

    def delete(self):
        """
        Deletes item from redis \n
        :return: None
        """
        if not self.idkey:
            raise KeyError("First you must save to remove it")
        self.Meta.connector.remove(self.idkey)

    @classmethod
    def get_tag_keys(cls, tag: str) -> List[str]:
        """
        returns keys tagged bay given tag\n
        :return: list
        """
        return cls.Meta.connector.gettagkeys(tag)

    @classmethod
    def get_tags(cls) -> List[str]:
        """
        returns tag list\n
        :return: list
        """
        return cls.Meta.connector.tags()

    @classmethod
    def get_by_tag(cls, tag: str) -> List['BaseNoSqlModel']:
        """
        returns obejct list tagged by given tag\n
        :return:[BaseNosqlModel]
        """
        retlist = []
        for itemdict in cls.Meta.connector.gettag(tag):
            if isinstance(itemdict, dict):
                retobj = cls()
                retobj.from_dict(itemdict)
                retlist.append(retobj)
        return retlist

    def add_tags_to_item(self, taglist: List[str]):
        """
        adds tags to object\n
        :param taglist: list of tags
        :return:
        """
        if not self.idkey:
            raise KeyError("You must save before adding a tag")
        for tag in taglist:
            self.Meta.connector.addtag(tag, self.idkey)

    def remove_item_from_tag(self, tag: str):
        """
        removes item from tag\n
        :param tag:
        :return:
        """
        if not self.idkey:
            raise KeyError("You must save before removing from a tag")
        self.Meta.connector.removefromtag(tag, self.idkey)

    def from_dict(self, updatedict: Dict[str, Any]):
        """
        populates data from dict
        Warning this will also overrides the id too!!        \n
        :param updatedict: dict which contains data
        :return: None
        """
        try:
            del updatedict["connector"]
        except (KeyError, TypeError):
            pass
        super().from_dict(updatedict.copy())

    def to_dict(self) -> Dict[str, Any]:
        """
        populates data to dict \n
        :return: None
        """
        retval = super().to_dict()
        try:
            del retval["connector"]
        except (KeyError, TypeError):
            pass
        return retval

    @classmethod
    def export_to_json_text(
            cls, exportdict: Dict[str, Dict[str, Any]] = None, compress_data=False) -> str:
        """
         transforms exportdict or whole database into json \n
        :param compress_data: bool, data will be compressed or not
        :param exportdict: must be dictionary of same class objects or json serializable values
        :return: returns a json compliant text file
        """
        edict: Dict[str, Optional[Dict[str, Any]]] = {}
        if exportdict:
            for key, value in exportdict.items():
                try:
                    if isinstance(value, cls):
                        edict[key] = value.to_dict()
                    else:
                        edict[key] = value
                except AttributeError:
                    pass
        else:
            edict = cls.Meta.connector.get_all_as_dict()
        if compress_data:
            for key, subdict in edict.items():
                if isinstance(subdict, dict):
                    edict[key] = dict((i, d) for i, d in subdict.items() if d)

            retval = json.dumps(edict, ensure_ascii=False, indent=4)
        else:
            retval = json.dumps(edict, ensure_ascii=False)
        return retval

    @classmethod
    def export_to_json_file(
            cls, filepath: str, exportdict: Dict[str, Dict[str, Any]] = None, compress_data=False):
        """
         transforms exportdict or whole database into *.json file \n
        :param filepath: must end with .json
        :param exportdict: must be dictionary of same class objects
        :param compress_data: bool, data will be compressed or not
        :return:
        """
        if not filepath.endswith(".json"):
            raise FileNotFoundError("Wrong filename:" + filepath)
        with open(filepath, "w", encoding="UTF-8") as ofile:
            ofile.write(cls.export_to_json_text(exportdict, compress_data=compress_data))

    @classmethod
    def export_to_json_zip(
            cls, filepath: str, exportdict: Dict[str, Dict[str, Any]] = None, compress_data=False):
        """
         transforms exportdict or whole database into *.zip file \n
        :param filepath: must be end with .zip
        :param exportdict: must be dictionary of same class objects
        :param compress_data: bool, data will be compressed or not
        :return:
        """
        if not filepath.endswith(".zip"):
            raise FileNotFoundError("Wrong filename:" + filepath)
        tempfilepath = filepath.replace(".zip", ".json")
        cls.export_to_json_file(tempfilepath, exportdict, compress_data=compress_data)
        zipfile.ZipFile(filepath, mode='w').write(tempfilepath)
        os.remove(tempfilepath)

    @classmethod
    def import_from_json_text(cls, jsontext: str):
        """
        import and update db from exported json text \n
        :param jsontext: exported json text
        :return:
        """
        datadict = json.loads(jsontext)
        for _, value in datadict.items():
            instance = cls()
            instance.from_dict(value)
            instance.save_to_cache()

    @classmethod
    def import_from_json_file(cls, filepath: str):
        """
        import and update db from exported *.json file \n
        :param filepath: exported *.json file
        :return:
        """
        with open(filepath, encoding="UTF-8") as ofile:
            content = ofile.read()
            cls.import_from_json_text(content)

    @classmethod
    def import_from_json_zip(cls, filepath: str):
        """
        import and update db from exported *.json file \n
        :param filepath: exported *.json file
        :return:
        """
        if not filepath.endswith(".zip"):
            raise FileNotFoundError("Wrong filename:" + filepath)

        tempfilepath = filepath.replace(".zip", ".json")
        with zipfile.ZipFile(filepath) as zip_obj:
            zip_obj.extractall("/")
        cls.import_from_json_file(tempfilepath)
        os.remove(tempfilepath)
