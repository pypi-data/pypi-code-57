"""
Basic dynamodb connector
"""
import time
from decimal import Decimal
from typing import Union, Dict, Any, List, Optional

# noinspection Mypy
import boto3
# from boto3.resources.factory.dynamodb import Table
# noinspection Mypy
from boto3.dynamodb.conditions import Key  # noqa
# noinspection Mypy
from botocore.exceptions import ClientError  # noqa

from nosqlmodel.connectors.baseconnector import BaseNosqlConnector

__author__ = 'ozgur'
__creation_date__ = '9.09.2019' '10:07'

D_REGION_NAME = ""
D_AWS_ACCESS_KEY_ID = ""
D_AWS_SECRET_ACCESS_KEY = ""


class DynamoConnector(BaseNosqlConnector):
    """    Dynamodb connector    """

    def __init__(self, tablename: str, region: str = None, access_key_id: str = None,
                 access_key_secret: str = None):
        drn = region if region else D_REGION_NAME
        aci = access_key_id if access_key_id else D_AWS_ACCESS_KEY_ID
        acs = access_key_secret if access_key_secret else D_AWS_SECRET_ACCESS_KEY

        self.source = boto3.resource(
            'dynamodb',
            region_name=drn,
            aws_access_key_id=aci,
            aws_secret_access_key=acs
        )
        self.tablename = tablename
        # self.table: Table = self.source.Table(tablename)  # pylint: disable=E1101
        self.table = self.source.Table(tablename)  # pylint: disable=E1101
        self.taglistkey = "tags"

        super().__init__()

    @staticmethod
    def _f_to_d(fval: float) -> Decimal:
        """
        float to decimal converter \n
        :param fval: float value
        :return: Decimal
        """
        return Decimal(str(fval))

    @staticmethod
    def _d_to_f(dval: Decimal) -> Union[float, int]:
        """
        Deciaml to float converter \n
        :param dval: Decimal value
        :return: float or int
        """
        try:
            if int(str(dval).split(".")[1]) == 0:
                retval = int(dval)
            else:
                # noinspection Mypy
                retval = float(dval)
        except IndexError:
            retval = int(dval)
        return retval

    def _d_to_f_dict(self, target: dict) -> dict:
        """
        checks items in dict and converts them to float if decimal \n
        :param target: raw dict
        :return: converted dict
        """
        if target:
            for key, value in target.items():
                if isinstance(value, Decimal):
                    target[key] = self._d_to_f(value)
        return target

    def delete_table(self):
        """
        deletes table from db\n
        :return:
        """
        try:
            self.table.delete()
            time.sleep(10)
        except ClientError:
            pass

    def create_table(self):
        """
        creates a new table, delete first if exists \n
        :return:
        """
        self.table = self.source.create_table(  # pylint: disable=E1101
            TableName=self.tablename,
            KeySchema=[
                {
                    'AttributeName': 'idkey',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'idkey',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        time.sleep(10)

    @staticmethod
    def issuccess(resp: dict) -> bool:
        """
        checks if request is success (returns 200)\n
        :param resp: boto response dict
        :return: bool
        """
        return resp.get("ResponseMetadata", {}).get("HTTPStatusCode", 0) == 200

    def keys(self, pattern='*') -> List[str]:
        """
        returns keys list in db \n
        :param pattern: str urlpathregex
        :return: the keys in db
        """
        retlist = []
        resp = self.table.scan(
            ProjectionExpression='idkey',
        )
        data = resp['Items']

        while 'LastEvaluatedKey' in resp:
            resp = self.table.scan(
                ExclusiveStartKey=resp['LastEvaluatedKey'],
                ProjectionExpression='idkey',
            )
            data.extend(resp['Items'])

        for rdict in data:
            val = str(rdict['idkey'])
            if not str(val).startswith(self.tagprefix):
                retlist.append(val)
        return retlist

    def dbsize(self) -> int:
        """
        returns the itemcount in db\n
        :return: item count
        """
        return len(self.keys())

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        get value by key\n
        :param key: str
        :return: dict or None
        """
        key = str(key)
        retval = self.table.get_item(
            Key={
                'idkey': key
            }
        ).get("Item", None)
        retval = self._d_to_f_dict(retval)

        return retval

    def get_multi(self, keylist: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        get value by key\n
        :param keylist: list of strings
        :return: [objectdict]
        """
        gsize = 99

        retdict: Dict[str, Dict[str, Any]] = {}
        for keygroup in [keylist[i:i + gsize] for i in range(0, len(keylist), gsize)]:
            keys = []
            for key in keygroup:
                keys.append({"idkey": str(key)})

            request_object = {
                self.tablename: {
                    'Keys': keys,
                    'ConsistentRead': True
                }
            }

            response = self.source.batch_get_item(  # pylint: disable=no-member
                RequestItems=request_object,
                ReturnConsumedCapacity='TOTAL'
            )
            retlist = response['Responses'][self.tablename]
            for itemdict in retlist:
                retdict[itemdict["idkey"]] = self._d_to_f_dict(itemdict)
        return retdict

    def get_all_as_list(self) -> List[Optional[Dict[str, Any]]]:
        """
        get all values in store \n
        :return: list
        """
        retlist: List[Optional[Dict[str, Any]]] = []
        for _, datadict in self.get_all_as_dict().items():
            retlist.append(datadict)

        return retlist

    def get_all_as_dict(self) -> Dict[str, Optional[Dict[str, Any]]]:
        """
        get all values in store \n
        :return: dict
        """

        resp = self.table.scan()
        data = resp['Items']
        retval: Dict[str, Optional[Dict[str, Any]]] = {}

        while 'LastEvaluatedKey' in resp:
            resp = self.table.scan(
                ExclusiveStartKey=resp['LastEvaluatedKey']
            )
            data.extend(resp['Items'])
        for ddict in data:
            if not str(ddict["idkey"]).startswith(self.tagprefix):
                for key, value in ddict.items():
                    if isinstance(value, Decimal):
                        ddict[key] = self._d_to_f(value)
                retval[str(ddict["idkey"])] = ddict

        return retval

    @classmethod
    def _get_upsert_check(cls, key: str, value: Dict[str, Any]) -> Dict[str, Any]:
        """
        checks item before insert and returns converted item\n
        :param key:
        :param value:
        :return:
        """

        if not isinstance(value, dict):
            raise TypeError("value must be dict but got" + str(type(value)))
        retval = value.copy()
        if "idkey" not in retval or not retval["idkey"]:
            retval["idkey"] = key

        for ikey, data in retval.items():
            if isinstance(data, float):
                retval[ikey] = cls._f_to_d(data)
        return retval

    def upsert(self, key: str, value: Dict[str, Any]) -> bool:
        """
        get all values in store \n
        :return: list
        """
        updict = self._get_upsert_check(key, value)
        resp = self.table.put_item(Item=updict)
        return self.issuccess(resp)

    def upsert_multi(self, itemdict: Dict[str, Dict[str, Any]]):
        """
        upsert multiple items at once\n
        :param itemdict: dict of objects dictionaries
        :return: bool
        """
        with self.table.batch_writer(overwrite_by_pkeys=['idkey']) as batch:
            for key, value in itemdict.items():
                updict = self._get_upsert_check(key, value)
                batch.put_item(updict)

    def remove(self, key: str) -> bool:
        """
        removes the key from store\n
        :param key: str or list or tuple
        :return:
        """
        resp = self.table.delete_item(
            Key={
                'idkey': str(key),
            }
        )
        return self.issuccess(resp)

    def remove_keys(self, keys: List[str]) -> bool:
        """
        removes the key from store\n
        :param keys:
        :return:
        """
        with self.table.batch_writer() as batch:
            for key in keys:
                batch.delete_item(Key={'idkey': str(key)})
        return True

    def flush(self):
        """
        Flushes current store\n
        :return: None
        """
        records = self.keys()
        records += [self.tagprefix + tag for tag in self.tags()]
        with self.table.batch_writer() as batch:
            for key in records:
                batch.delete_item(Key={'idkey': key})

    def tags(self) -> List[str]:
        """
        returns tag list \n
        :return:
        """
        fexppr = Key("idkey").begins_with(self.tagprefix)
        resp = self.table.scan(
            FilterExpression=fexppr,
            ProjectionExpression='idkey',
        )
        data = resp['Items']

        while 'LastEvaluatedKey' in resp:
            resp = self.table.scan(
                FilterExpression=fexppr,
                ProjectionExpression='idkey',
                ExclusiveStartKey=resp['LastEvaluatedKey']
            )
            data.extend(resp['Items'])
        for index, ddict in enumerate(data):
            data[index] = ddict

        return [rdict['idkey'].replace(self.tagprefix, "", 1) for rdict in data]

    def gettagkeys(self, tag: str) -> List[str]:
        """
        get all keys of given tag \n
        :param tag:
        :return:
        """
        tdict = self.get(self.tagprefix + tag)
        retval = tdict[self.taglistkey] if tdict else []
        return retval

    def gettag(self, tag: str) -> List[Optional[Dict[str, Any]]]:
        """
        get all dict items in given tag \n
        :param tag:
        :return: list of dictionaries
        """
        retlist = []
        memberids = self.gettagkeys(tag)
        for memberid in list(memberids):
            retlist.append(self.get(memberid))

        return retlist

    def addtag(self, tag: str, key: str):
        """
        Adds tags to keys \n
        :param tag: list
        :param key: list
        :return: None
        """
        if not (tag and key):
            raise TypeError
        tags = self.gettagkeys(tag)
        tags.append(key)
        tags = list(set(tags))
        ukey = self.tagprefix + tag
        self.upsert(ukey, {"idkey": ukey, self.taglistkey: tags})

    def removefromtag(self, tag: str, key: Union[str, list]):
        """
        Remove items from lists \n
        :param tag: str
        :param key: str or list
        :return: None
        """

        tags = list(set(self.gettagkeys(tag)))
        if isinstance(key, str):
            # noinspection PyBroadException
            try:
                tags.remove(key)
            except Exception:  # pylint: disable=broad-except
                pass
        else:
            for k in key:
                # noinspection PyBroadException
                try:
                    tags.remove(k)
                except Exception:  # pylint: disable=broad-except
                    pass

        ukey = self.tagprefix + tag
        self.upsert(ukey, {"idkey": ukey, self.taglistkey: tags})
