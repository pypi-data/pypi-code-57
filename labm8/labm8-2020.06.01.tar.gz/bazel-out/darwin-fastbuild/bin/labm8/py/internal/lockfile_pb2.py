# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: labm8/py/internal/lockfile.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='labm8/py/internal/lockfile.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n labm8/py/internal/lockfile.proto\"\xe6\x01\n\x08LockFile\x12(\n\x10owner_process_id\x18\x01 \x01(\x05R\x0eownerProcessId\x12,\n\x12owner_process_argv\x18\x02 \x01(\tR\x10ownerProcessArgv\x12<\n\x1b\x64\x61te_acquired_unix_epoch_ms\x18\x03 \x01(\x03R\x17\x64\x61teAcquiredUnixEpochMs\x12%\n\x0eowner_hostname\x18\x04 \x01(\tR\rownerHostname\x12\x1d\n\nowner_user\x18\x05 \x01(\tR\townerUser')
)




_LOCKFILE = _descriptor.Descriptor(
  name='LockFile',
  full_name='LockFile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='owner_process_id', full_name='LockFile.owner_process_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='ownerProcessId', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owner_process_argv', full_name='LockFile.owner_process_argv', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='ownerProcessArgv', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date_acquired_unix_epoch_ms', full_name='LockFile.date_acquired_unix_epoch_ms', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='dateAcquiredUnixEpochMs', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owner_hostname', full_name='LockFile.owner_hostname', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='ownerHostname', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owner_user', full_name='LockFile.owner_user', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='ownerUser', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=37,
  serialized_end=267,
)

DESCRIPTOR.message_types_by_name['LockFile'] = _LOCKFILE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LockFile = _reflection.GeneratedProtocolMessageType('LockFile', (_message.Message,), dict(
  DESCRIPTOR = _LOCKFILE,
  __module__ = 'labm8.py.internal.lockfile_pb2'
  # @@protoc_insertion_point(class_scope:LockFile)
  ))
_sym_db.RegisterMessage(LockFile)


# @@protoc_insertion_point(module_scope)
