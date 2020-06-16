import logging

from functools import wraps
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient
from pymongo import MongoClient

from .document_dict import DocumentDict
from .document_array import DocumentArray

LOG = logging.getLogger("mdocument")


def check_setup(func):
    """Decorator for checking that document have valid loop and client."""

    async def arg_wrap(cls, *args, **kwargs):
        self = None
        if not isinstance(cls, type):
            self = cls
            cls = cls.__class__
        if "client" not in cls.__dict__:
            raise ClientNotFound()
        elif "database" not in cls.__dict__:
            raise DocumentException("Required attribute database is missing.")
        elif "collection" not in cls.__dict__:
            raise DocumentException("Required attribute collection is missing.")
        return await func(self, *args, **kwargs) if self else await func(cls, *args, **kwargs)

    return arg_wrap


class DocumentException(Exception):
    def __init__(self, message):
        self.message = message


class DocumentDoesntExist(DocumentException):
    def __init__(self):
        super().__init__("Document not found")


class ClientNotFound(DocumentException):
    def __init__(self):
        super().__init__("Client is not provided. Can't connect to database.")


class DocumentField:

    def __init__(self, document_cls, name=None, parent=False):
        self.document_cls = document_cls
        self.name = name
        self.parent = parent

    def __getattr__(self, item):
        return DocumentField(self.document_cls, item)

    def __getitem__(self, item):
        pass

    def __repr__(self):
        return f"{self.document_cls.__name__}.{self.name}"

    def __eq__(self, other: "DocumentField"):
        try:
            return self.document_cls is other.document_cls and self.name == other.name
        except AttributeError:
            raise TypeError(f"Can't compare {other} to DocumentField.")


class DocumentRelations:
    def __init__(self):
        self.relations = []

    def add(self, document_func, first_document_field_name: str,
            second_document_field: DocumentField, parent) -> None:
        """Adds new document relation."""

        self.relations.append({
            "document_func": document_func,
            "first_document_field_name": first_document_field_name,
            "second_document_field": second_document_field,
            "first_is_parent": parent
        })

    def search_by_field(self, field: DocumentField):
        """Search for related fields by DocumentField."""

        related_to_field = []
        for relation in self.relations:
            first_document: type = relation["document_func"](None)
            second_document_field: DocumentField = relation["second_document_field"]
            if (field.document_cls is first_document
                    and field.name == relation["first_document_field_name"]):
                related_to_field.append(second_document_field)
            elif field == second_document_field:
                related_to_field.append(
                    DocumentField(first_document, relation["first_document_field_name"],
                                  not relation["first_is_parent"]))
        return related_to_field

    def search_by_document(self, document: "Document"):
        """Search for related fields by DocumentField."""

        related_field = []
        for relation in self.relations:
            first_document: type = relation["document_func"](None)
            second_document_field: DocumentField = relation["second_document_field"]
            if document.__class__ is first_document:
                first_document_field = DocumentField(document.__class__,
                                                     relation["first_document_field_name"],
                                                     relation["first_is_parent"])
                related_field.append([first_document_field, second_document_field])
            elif second_document_field.document_cls is document.__class__:

                first_document_field = DocumentField(first_document,
                                                     relation["first_document_field_name"],
                                                     relation["first_is_parent"])
                related_field.append([second_document_field, first_document_field])
        return related_field


class MetaDocument(type):
    database: str
    collection: str
    client: AsyncIOMotorClient
    collection: AsyncIOMotorCollection

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.create_indexes()

    @property
    def collection(cls) -> AsyncIOMotorCollection:
        for field in ("client", "database", "collection"):
            if field not in cls.__dict__:
                raise type("{}NotFound".format(field.capitalize()), (DocumentException,), {})(
                    f"Required attribute {field} is missing."
                )

        client = cls.__dict__["client"]
        database = cls.__dict__["database"]
        collection = cls.__dict__["collection"]

        return client[database][collection]

    @property
    def sync_collection(cls):
        for field in ("client", "database", "collection"):
            if field not in cls.__dict__:
                raise type("{}NotFound".format(field.capitalize()), (DocumentException,), {})(
                    f"Required attribute {field} is missing."
                )

        client = cls.__dict__["client"]
        database = cls.__dict__["database"]
        collection = cls.__dict__["collection"]
        return client.delegate[database][collection]

    def __getattribute__(cls, item: str):
        if item in ("database", "client"):
            raise AttributeError(item)
        return super().__getattribute__(item)

    @property
    def Field(cls):
        return DocumentField(cls)

    def create_indexes(cls):
        """Called on class creation. Made for automatic indexes creation.
        Can be implemented in subclass (Optional).
        Here cls.sync_collection should be used.
        """


class Document(metaclass=MetaDocument):
    Relations = DocumentRelations()

    def __init__(self, **kwargs):
        super().__setattr__("_document_", DocumentDict(kwargs))
        super().__setattr__("shadow_copy", DocumentDict(kwargs.copy()))

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(f"{key}={value}" for key, value in self._document_.items())
        )

    def __getattribute__(self, item):
        if item in ("collection", "database", "client"):
            if item in self._document_:
                return self._document_[item]
            raise AttributeError()
        return super().__getattribute__(item)

    def __getattr__(self, item, special=False):
        try:
            if isinstance(self._document_[item], dict):
                return DocumentDict(self._document_[item])
            elif isinstance(self._document_[item], list):
                return DocumentArray(self._document_[item])
            return self._document_[item]
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, key, value):
        self._document_[key] = value

    def __delattr__(self, item):
        del self._document_[item]

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __getitem__(self, item):
        return self._document_[item]

    def __delitem__(self, key):
        return delattr(self, key)

    def __iter__(self):
        return iter(self._document_)

    def __eq__(self, other):
        return self._document_ == other

    def keys(self):
        return self._document_.keys()

    def items(self):
        return DocumentDict(self._document_).items()

    async def _update_related(self):
        """Force updates related fields in other documents."""

        related_fields = self.Relations.search_by_document(self)

        for self_field, other_field in related_fields:
            if self_field.parent:
                for document in await other_field.document_cls.many({
                        other_field.name: self.shadow_copy[self_field.name]}):
                    document[other_field.name] = self[self_field.name]
                    await document.push_update()

    @check_setup
    async def push_update(self):
        """Force update document."""

        await self._update_related()
        return await self.__class__.collection.replace_one(
            {"_id": self.shadow_copy._id}, self._document_)

    @classmethod
    @check_setup
    async def exists(cls, *args, **kwargs):
        """Checks that document exists."""

        if await cls.collection.find_one(*args, **kwargs):
            return True
        return False

    @classmethod
    @check_setup
    async def one(cls, **kwargs):
        """Finds one document based on kwargs."""

        document = await cls.collection.find_one(kwargs)
        if not document:
            raise DocumentDoesntExist()
        return cls(**document)

    @classmethod
    @check_setup
    async def many(cls, **kwargs) -> list:
        """Finds multiple documents based on kwargs."""

        result_list = []
        cursor = cls.collection.find(kwargs)
        async for doc in cursor:
            result_list.append(cls(**doc))
        return result_list

    @classmethod
    @check_setup
    async def create(cls, **kwargs) -> "Document":
        """Create new document."""

        await cls.collection.insert_one(kwargs)
        return cls(**kwargs)

    async def _delete_related(self):
        """Deletes related documents or pops field values."""

        related_fields = self.Relations.search_by_document(self)

        for self_field, other_field in related_fields:
            if self_field.parent:
                for document in await other_field.document_cls.many(**{
                        other_field.name: self[self_field.name]}):
                    await document.delete()

    async def delete(self):
        """Delete current document and related fields or documents base on related."""

        result = await self.__class__.collection.delete_one({"_id": self._id})
        await self._delete_related()
        return result

    @staticmethod
    def related(other_field: DocumentField, multiple=True, parent=True, self_field_name=None,
                other_is_parent=False):
        """Decorator for related documents.

        :param other_is_parent: defines that other document is a Parent
        :param parent: show relations type. When Parent updated or deleted Child is also updated
        and deleted. When Child is updated or deleted Parent stays the same.
        :param self_field_name: ThisDocument field pk for OtherDocument field
        :param other_field: DocumentField path to other document
        :param multiple: return multiple documents or only one
        """

        def func_wrapper(func):

            other_field.parent = other_is_parent

            self_field = self_field_name if self_field_name else func.__name__
            Document.Relations.add(func, self_field, other_field, parent)

            @wraps(func)
            async def fget(self):
                field = DocumentField(self.__class__, self_field)

                try:
                    if multiple:
                        return await other_field.document_cls.many(
                            **{other_field.name: self._document_.get(field.name)})
                    else:
                        return await other_field.document_cls.one(
                            **{other_field.name: self._document_.get(field.name)})
                except DocumentDoesntExist:
                    return

            result = property(fget=fget)

            return result

        return func_wrapper
