# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
TODO: this patch is only necessary for the protect rule. The assess rule is completely
handled by policy.
"""
from functools import partial

from contrast.extern.wrapt import register_post_import_hook
from contrast.applies import (
    ACTION_DELETE,
    ACTION_FIND,
    ACTION_INSERT_MANY,
    ACTION_INSERT_ONE,
    ACTION_UPDATE,
    DATABASE_MONGO,
)
from contrast.applies.common.applies_nosqli_rule import apply_rule
from contrast.utils.patch_utils import patch_cls_or_instance

INSERT_ONE = "insert_one"
INSERT_MANY = "insert_many"
# Mongo suggest calling either update_one or update_many, but both call
# self._update_retryable() Similar situation with find, replace_one, delete_one,
# delete_many  and find_many (both just end up calling find) INSERT is the only
# difference where they call difference methods based on one or many.
UPDATE = "_update_retryable"
FIND = "find"
DELETE = "_delete_retryable"


apply_nosqli = partial(apply_rule, DATABASE_MONGO)


def insert_one(original, patch_policy=None, *args, **kwargs):
    return apply_nosqli(ACTION_INSERT_ONE, original, args, kwargs)


def insert_many(original, patch_policy=None, *args, **kwargs):
    return apply_nosqli(ACTION_INSERT_MANY, original, args, kwargs)


def update(original, patch_policy=None, *args, **kwargs):
    return apply_nosqli(ACTION_UPDATE, original, args, kwargs)


def find(original, patch_policy=None, *args, **kwargs):
    return apply_nosqli(ACTION_FIND, original, args, kwargs)


def delete(original, patch_policy=None, *args, **kwargs):
    return apply_nosqli(ACTION_DELETE, original, args, kwargs)


def patch_pymongo(collection_module):
    patch_cls_or_instance(collection_module.Collection, INSERT_ONE, insert_one)
    patch_cls_or_instance(collection_module.Collection, INSERT_MANY, insert_many)
    patch_cls_or_instance(collection_module.Collection, FIND, find)
    patch_cls_or_instance(collection_module.Collection, DELETE, delete)
    patch_cls_or_instance(collection_module.Collection, UPDATE, update)


def register_patches():
    register_post_import_hook(patch_pymongo, "pymongo.collection")
