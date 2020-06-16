from typing import Any, List, Optional, Type

from bson import CodecOptions
from motor.motor_asyncio import AsyncIOMotorClient

# from pymongo.client_session import ClientSession
from pymongo.collection import Collection

# from pymongo.cursor import Cursor
# from pymongo.results import InsertOneResult, UpdateResult

from fa_common import get_current_app, get_timezone
from fa_common import logger as LOG

from .base_client import BaseClient
from .models import (
    DeleteResult,
    FireOffset,
    Operator,
    SortOrder,
    WhereCondition,
    WriteResult,
    DocumentDBModel,
)

# FIXME missing base class methods
class MongoDBClient(BaseClient):
    """
    Singleton client for interacting with MongoDB.
    Operates mostly using models, specified when making DB queries.

    Implements only part of internal `motor` methods, but can be populated more.

    Please don't use it directly, use `scidra.core.db.utils.get_db_client`.
    """

    __instance = None
    mongodb: AsyncIOMotorClient = None

    def __new__(cls) -> "MongoDBClient":
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            app = get_current_app()
            tzinfo = get_timezone()
            cls.__instance.codec_options = CodecOptions(tz_aware=True, tzinfo=tzinfo)
            cls.__instance.mongodb = app.mongodb  # type: ignore
        return cls.__instance

    def get_collection(self, collection_name: str) -> Collection:
        return self.mongodb.get_collection(
            collection_name, codec_options=self.codec_options
        )

    async def insert(
        self, model: DocumentDBModel, include=None, exclude=None, session: Any = None,
    ) -> WriteResult:
        data = model.dict(include=include, exclude=exclude)
        data["_id"] = data.pop("id")
        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        result: InsertOneResult = await collection.insert_one(data, session=session)

        LOG.info("Insert Result: {}", result)
        # FIXME: Correct result return
        return WriteResult()

    async def count(self, model: Type[DocumentDBModel], session: Any = None) -> int:

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        res = await collection.count_documents(session=session)
        return res

    async def delete(
        self, model: Type[DocumentDBModel], _id: str, session: Any = None
    ) -> DeleteResult:

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        res = await collection.delete_one(_id=_id, session=session)
        return DeleteResult()

    async def update_one(
        self, model: Type[DocumentDBModel], _id: str, data: dict, session: Any = None
    ) -> WriteResult:
        data.pop("id", None)
        if _id is not None:
            data["_id"] = _id

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        await collection.update_one(filter={"_id": _id}, update=data, session=session)
        return WriteResult()

    # FIXME: Add this back once the firstore version has been fixed and added
    # async def update_many(
    #     self, model: Type[DocumentDBModel], data: List[Tuple[str, dict]]
    # ) -> WriteResult:
    #     _id = filter_kwargs.pop("id", None)
    #     if _id is not None:
    #         filter_kwargs["_id"] = _id

    #     collection_name = model.get_db_collection()
    #     collection = self.get_collection(collection_name)
    #     res = await collection.update_many(filter_kwargs, kwargs, session=session)
    #     return res

    async def get(
        self, model: Type[DocumentDBModel], _id: str, session: Any = None
    ) -> Optional[DocumentDBModel]:

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)
        res = await collection.find_one(_id=_id, session=session)
        if res is None:
            return None

        return model(**res)

    async def list(
        self,
        model: Type[DocumentDBModel],
        where: List[WhereCondition] = [],
        _limit: int = 0,
        _sort: List[Tuple[str, SortOrder]] = None,
        mongo_offset: int = 0,
        fire_offset: FireOffset = None,
    ) -> List[DocumentDBModel]:

        _id = kwargs.pop("id", None)
        if _id is not None:
            kwargs["_id"] = _id

        collection_name = model.get_db_collection()
        collection = self.get_collection(collection_name)

        filter_dict = {}
        for wc in where:
            if wc.operator is Operator.EQUALS:
                filter_dict[wc.field] = wc.value
            elif wc.operator is Operator.LT:
                filter_dict[wc.field] = {"$lt": wc.value}
            elif wc.operator is Operator.GT:
                filter_dict[wc.field] = {"$gt": wc.value}
            # TODO: Other array filters

        finder = collection.find(filter_dict, skip=mongo_offset, limit=_limit)
        if _sort is not None:
            for sort in _sort:
                finder.sort(sort[0], sort[1])
        results = await finder.to_list()
        models: List[DocumentDBModel] = []
        for res in results:
            models.append(model(**res))
        return models
