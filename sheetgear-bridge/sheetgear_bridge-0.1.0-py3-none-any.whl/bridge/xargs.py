#!/usr/bin/env python3

import os

from sheetgear.bridge.utils import pick_object_fields

def create_spreadsheet_argspec():
  argument_spec = dict(
    spreadsheet_id = dict(type='str', required=False, default=os.environ.get('SHEETGEAR_SPREADSHEET_ID', '')),
    client_secrets_file = dict(type='str', require=False, default=os.environ.get('SHEETGEAR_CLIENT_SECRETS_FILE', '')),
    credentials_file = dict(type='str', require=False, default=os.environ.get('SHEETGEAR_CREDENTIALS_FILE', '')),
  )
  return argument_spec

def extract_spreadsheet_args(params):
  constructor_args = pick_object_fields(params, ['spreadsheet_id', 'client_secrets_file', 'credentials_file'])
  return constructor_args


def create_sheet_argspec():
  argument_spec = create_spreadsheet_argspec()
  argument_spec.update(dict(
    sheet_name = dict(type='str', require=False, default=os.environ.get('SHEETGEAR_SHEET_NAME', '')),
  ))
  return argument_spec

def extract_sheet_args(params):
  constructor_args = extract_spreadsheet_args(params)
  sheet_args = pick_object_fields(params, ['sheet_name'])
  return constructor_args, sheet_args


def create_frame_range_argspec():
  argument_spec = create_sheet_argspec()
  argument_spec.update(dict(
    frame_range = dict(type='dict',options = dict(
      left_col = dict(type='str', require=True, default='A'),
      right_col = dict(type='str', require=True),
      begin_row = dict(type='int', require=True, default=1),
      start_row = dict(type='int', require=False),
      end_row = dict(type='int', require=False),
    )),
  ))
  return argument_spec

def extract_frame_range_args(params):
  constructor_args, sheet_args = extract_sheet_args(params)
  action_args = pick_object_fields(params, ['frame_range'])
  return constructor_args, sheet_args, action_args


def create_range_delete_argspec():
  argument_spec = create_frame_range_argspec()
  argument_spec.update(dict(
    start_row=dict(type='int', require=True),
    length=dict(type='int', require=True),
  ))
  return argument_spec

def extract_range_delete_args(params):
  constructor_args, sheet_args = extract_sheet_args(params)
  action_args = pick_object_fields(params, ['frame_range', 'start_row', 'length'])
  return constructor_args, sheet_args, action_args


def create_range_append_argspec():
  argument_spec = create_frame_range_argspec()
  argument_spec.update(dict(
    field_mappings=dict(type='dict', require=False, default=dict()),
    records=dict(type='list', require=True),
    includes=dict(type='list', require=False),
    excludes=dict(type='list', require=False),
  ))
  return argument_spec

def extract_range_append_args(params):
  constructor_args, sheet_args = extract_sheet_args(params)
  action_args = pick_object_fields(params, ['frame_range', 'field_mappings', 'records', 'includes', 'excludes', 'options'])
  return constructor_args, sheet_args, action_args


def create_range_modify_argspec():
  argument_spec = create_frame_range_argspec()
  argument_spec.update(dict(
    field_mappings=dict(type='dict', require=False, default=dict()),
    start_row=dict(type='int', require=True),
    records=dict(type='list', require=True),
    includes=dict(type='list', require=False),
    excludes=dict(type='list', require=False),
  ))
  return argument_spec

def extract_range_modify_args(params):
  constructor_args, sheet_args = extract_sheet_args(params)
  action_args = pick_object_fields(params, ['frame_range', 'field_mappings', 'start_row', 'records', 'includes', 'excludes', 'options'])
  return constructor_args, sheet_args, action_args


def create_range_fetch_argspec():
  argument_spec = create_frame_range_argspec()
  argument_spec.update(dict(
    field_mappings=dict(type='dict', require=False, default=dict()),
    includes=dict(type='list', require=False, default=[]),
    excludes=dict(type='list', require=False, default=[]),
    skip=dict(type='int', require=True, default=0),
    limit=dict(type='int', require=True, default=100),
    options=dict(type='dict', require=False, options=dict(
      dateTimeRenderOption=dict(type='str',require=False),
      valueRenderOption=dict(type='str',require=False),
    ))
  ))
  return argument_spec

def extract_range_fetch_args(params):
  constructor_args, sheet_args = extract_sheet_args(params)
  action_args = pick_object_fields(params, ['frame_range', 'field_mappings', 'includes', 'excludes', 'skip', 'limit', 'options'])
  return constructor_args, sheet_args, action_args


def create_range_query_argspec():
  argument_spec = create_range_fetch_argspec()
  argument_spec.update(dict(
    criteria=dict(type='list', require=False, default=[]),
  ))
  return argument_spec

def extract_range_query_args(params):
  constructor_args, sheet_args = extract_sheet_args(params)
  action_args = pick_object_fields(params, ['frame_range', 'field_mappings', 'criteria', 'includes', 'excludes', 'skip', 'limit', 'options'])
  return constructor_args, sheet_args, action_args


def create_range_modify_by_query_argspec():
  argument_spec = create_range_query_argspec()
  argument_spec.update(dict(
    record=dict(type='dict', require=True),
  ))
  return argument_spec

def extract_range_modify_by_query_args(params):
  constructor_args, sheet_args = extract_sheet_args(params)
  action_args = pick_object_fields(params, ['frame_range', 'field_mappings', 'criteria', 'record', 'includes', 'excludes', 'skip', 'limit', 'options'])
  return constructor_args, sheet_args, action_args
