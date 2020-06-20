#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import copy
import re
from googleapiclient import discovery
from sheetgear.bridge.errors import InvalidGridRangeError
from sheetgear.bridge.errors import SheetNotFoundError
from sheetgear.bridge.gauth import authorize
from sheetgear.bridge.utils import lookup_number_of_colname
from sheetgear.bridge.utils import lookup_colname_by_number
from sheetgear.bridge.utils import lookup_fieldname_from_mappings

DEFAULT_MAJOR_DIMENSION = 'ROWS'
DEFAULT_SHIFT_DIMENSION = 'ROWS'

DEFAULT_JUMP_STEP = 100

class Handler(object):
  """Handle the basic Spreadsheet API (initialize the parameters, authenticate the credentials, ...).
  """

  def __init__(self, **kwargs):
    self.__spreadsheet_id = kwargs['spreadsheet_id'] if 'spreadsheet_id' in kwargs else None
    assert isinstance(self.__spreadsheet_id, str) and len(self.__spreadsheet_id) > 0,\
        'spreadsheet_id must be a non-empty string'

    self.__client_secrets_info = kwargs['client_secrets_info'] if 'client_secrets_info' in kwargs else None
    assert self.__client_secrets_info is None or\
        isinstance(self.__client_secrets_info, dict) and len(self.__client_secrets_info) > 0,\
        'client_secrets_info must be a non-empty dictionary'

    self.__client_secrets_file = kwargs['client_secrets_file'] if 'client_secrets_file' in kwargs else None
    assert self.__client_secrets_file is None or\
        isinstance(self.__client_secrets_file, str) and len(self.__client_secrets_file) > 0,\
        'client_secrets_file must be a non-empty string'

    assert self.__client_secrets_info is not None or self.__client_secrets_file is not None,\
        'one of client_secrets_info and client_secrets_file options must be defined'

    self.__credentials_file = kwargs['credentials_file'] if 'credentials_file' in kwargs else None
    assert (isinstance(self.__credentials_file, str) and len(self.__credentials_file) > 0),\
        'credentials_file must be a non-empty string'
    pass


  @property
  def spreadsheet_id(self): 
    return self.__spreadsheet_id


  @property
  def properties(self): 
    request = self._dialect.get(
      spreadsheetId=self.spreadsheet_id,
      includeGridData=False
    )
    return request.execute()


  def _authorize(self):
    return authorize(self.__credentials_file,
      self.__client_secrets_file,
      self.__client_secrets_info)

  def loadToken(self):
    creds = self._authorize()
    return {
      'client_id': creds.client_id,
      'client_secret': creds.client_secret,
      'id_token': creds.id_token,
      'refresh_token': creds.refresh_token,
      'token_uri': creds.token_uri,
      'valid': creds.valid,
      'expired': creds.expired,
      'scopes': creds.scopes,
    }

  def openSheet(self, sheet_name):
    return Sheet(handler=self, sheet_name=sheet_name)

  @property
  def _service(self):
    return discovery.build('sheets', 'v4', credentials=self._authorize())

  @property
  def _dialect(self):
    return self._service.spreadsheets()


class Sheet(object):

  def __init__(self, **kwargs):
    self.__handler = kwargs['handler'] if 'handler' in kwargs else None
    assert isinstance(self.__handler, Handler),\
        'handler must be a Handler instance'

    self.__sheet_name = kwargs['sheet_name'] if 'sheet_name' in kwargs else None
    assert (isinstance(self.__sheet_name, str) and len(self.__sheet_name) > 0),\
        'sheet_name must be a non-empty string'

  @property
  def sheet_properties(self):
    info = self.__handler.properties
    if info is not None and 'sheets' in info and isinstance(info['sheets'], list):
      for sheetInfo in info['sheets']:
        if isinstance(sheetInfo, dict) and 'properties' in sheetInfo:
          props = sheetInfo['properties']
          if isinstance(props, dict) and 'title' in props and props['title'] == self.__sheet_name:
            return props
    return None

  @property
  def sheet_id(self):
    _prop = self.sheet_properties
    if _prop is None:
      raise SheetNotFoundError('Cannot get the sheet information')
    return _prop['sheetId']

  @property
  def sheet_name(self):
    return self.__sheet_name


  def count(self, frame_range):
    # determine the data-range
    frame = self.__newFrame(frame_range).without_bottom

    request = self.__dialect.values().get(
      spreadsheetId = self.__handler.spreadsheet_id,
      range = frame.a1_range
    )

    result = request.execute()
    values = result.get('values', [])

    return len(values)


  def query(self, frame_range, field_mappings, criteria, includes=None, excludes=None, skip=None, limit=None, options=dict()):
    restriction = options['restriction'] if isinstance(options, dict) and 'restriction' in options else 0
    skip = 0
    jump = DEFAULT_JUMP_STEP
    count = 0
    list = []
    while True:
      count = count + 1

      step = self.fetch(frame_range, field_mappings, includes=includes, excludes=excludes, skip=skip, limit=jump, options=options)

      data = step['data'] if 'data' in step else []

      size = len(data)
      if size == 0:
        break

      skip = skip + size

      for item in data:
        record = item['record']
        if self.match(record, criteria):
          list.append(item)

      if 0 < restriction and restriction < count:
        break

    return dict(data=list)


  def update_by_query(self, frame_range, field_mappings, criteria, record, skip=None, limit=None, includes=None, excludes=None, options=dict()):
    records = [ dict(record=record) ]
    _packet = self.query(frame_range, field_mappings, criteria, includes=includes, excludes=excludes, options=options)
    _data = _packet['data'] if 'data' in _packet else []
    _info = []
    for i in range(len(_data)):
      item = _data[-i-1]
      if isinstance(item, dict) and 'row_number' in item:
        frame_range['start_row'] = item['row_number']
        frame_range['end_row'] =  item['row_number']
        _info.append(self.update(frame_range, field_mappings, records, includes=includes, excludes=excludes, options=options))
    return _info


  def delete_by_query(self, frame_range, field_mappings, criteria, skip=None, limit=None, includes=None, excludes=None, options=dict()):
    _packet = self.query(frame_range, field_mappings, criteria, includes=includes, excludes=excludes, options=options)
    _data = _packet['data'] if 'data' in _packet else []
    _info = []
    for i in range(len(_data)):
      item = _data[-i-1]
      if isinstance(item, dict) and 'row_number' in item:
        frame_range['start_row'] = item['row_number']
        frame_range['end_row'] =  item['row_number']
        _info.append(self.delete(frame_range, options=options))
    return _info


  def match(self, record, criteria):
    if isinstance(criteria, list) and len(criteria) > 0:
      for crit in criteria:
        if 'field' in crit:
          _field_name = crit['field']
          if _field_name in record:
            _value = record[_field_name]
            if _value is not None:
              if 'equal' in crit:
                return str(_value) == crit['equal']
              if 'match' in crit:
                _r = re.match(crit['match'], str(_value), re.M|re.I)
                if _r:
                  return True
      return False
    else:
      return True


  def fetch(self, frame_range, field_mappings, includes=None, excludes=None, skip=None, limit=None, options=dict()):
    # determine the data-range
    frame = self.__newFrame(frame_range, field_mappings)

    if skip is not None:
      frame.skip = skip

    if limit is not None:
      frame.limit = limit

    params = dict(
      spreadsheetId = self.__handler.spreadsheet_id,
      range = frame.a1_range
    )

    if isinstance(options, dict):
      if 'valueRenderOption' in options:
        _v = options['valueRenderOption']
        if _v in ['FORMATTED_VALUE', 'UNFORMATTED_VALUE', 'FORMULA']:
          params['valueRenderOption'] = _v

      if 'dateTimeRenderOption' in options:
        _t = options['dateTimeRenderOption']
        if _t in ['FORMATTED_STRING', 'SERIAL_NUMBER']:
          params['dateTimeRenderOption'] = _t

    request = self.__dialect.values().get(**params)

    result = request.execute()
    values = result.get('values', [])

    _records = frame.convert_rows_to_records(values=values, includes=includes, excludes=excludes)

    data = []
    if isinstance(_records, list):
      _row_number = frame.start_row
      for _record in _records:
        data.append(dict(row_number=_row_number,record=_record))
        _row_number = _row_number + 1

    return dict(data=data)


  def append(self, frame_range, field_mappings, records, includes=None, excludes=None, options=dict()):
    # determine the data-range
    frame = self.__newFrame(frame_range, field_mappings)

    # generate the values
    values = frame.convert_records_to_rows(records, includes=includes, excludes=excludes)

    # update data to the new range
    request = self.__dialect.values().append(
        spreadsheetId=self.__handler.spreadsheet_id,
        valueInputOption='USER_ENTERED', #'RAW'
        insertDataOption='OVERWRITE', #'INSERT_ROWS'
        range=frame.a1_range,
        body=dict(majorDimension=DEFAULT_MAJOR_DIMENSION, values=values)
    )

    # apply dry_run mode
    if self.__dry_run_mode(options):
      return self.__dry_run_info(frame)

    # execute the request
    return dict(info=request.execute())


  def insert(self, frame_range, field_mappings, start_row, records, includes=None, excludes=None, options=dict()):
    return self.__upsert(
      frame_range=frame_range,
      field_mappings=field_mappings,
      start_row=start_row,
      records=records,
      includes=includes,
      excludes=excludes,
      options=options,
      flag=True)


  def update(self, frame_range, field_mappings, start_row, records, includes=None, excludes=None, options=dict()):
    return self.__upsert(
      frame_range=frame_range,
      field_mappings=field_mappings,
      start_row=start_row,
      records=records,
      includes=includes,
      excludes=excludes,
      options=options,
      flag=False)


  def __upsert(self, frame_range, field_mappings, start_row, records, includes=None, excludes=None, options=dict(), flag=True):
    assert len(records) > 0, 'records must not be empty'

    # determine the data-range
    frame = self.__newFrame(frame_range, field_mappings)

    frame.start_row = start_row
    frame.end_row = start_row + len(records) - 1

    _check_mode = self.__dry_run_mode(options)
    _dialect = self.__dialect

    if flag and not _check_mode:
      insertReq = _dialect.batchUpdate(
        spreadsheetId=self.__handler.spreadsheet_id,
        body=dict(
          requests=[
            dict(
              insertRange=dict(
                range=frame.grid_range,
                shiftDimension=DEFAULT_SHIFT_DIMENSION
              )
            )
          ]
        )
      )
      insertReq.execute()

    # generate the values
    values = frame.convert_records_to_rows(records, includes=includes, excludes=excludes)

    # update data to the new range
    request = _dialect.values().update(
        spreadsheetId=self.__handler.spreadsheet_id,
        valueInputOption='USER_ENTERED', #'RAW'
        range=frame.a1_range,
        body=dict(majorDimension=DEFAULT_MAJOR_DIMENSION, values=values)
    )

    # apply dry_run mode
    if _check_mode:
      return self.__dry_run_info(frame)

    # execute the request
    return dict(info=request.execute())


  def clear(self, frame_range, start_row, length, options=dict()):
    assert length > 0, 'length must be a positive integer'

    # determine the data-range
    frame = self.__newFrame(frame_range)

    frame.start_row = start_row
    frame.end_row = start_row + length - 1

    # update data to the new range
    request = self.__dialect.values().clear(
        spreadsheetId=self.__handler.spreadsheet_id,
        range=frame.a1_range,
        body=dict()
    )

    # apply dry_run mode
    if self.__dry_run_mode(options):
      return self.__dry_run_info(frame)

    # execute the request
    return dict(info=request.execute())


  def delete(self, frame_range, start_row, length, options=dict()):
    assert length > 0, '[length] must be a positive integer'

    # determine the data-range
    frame = self.__newFrame(frame_range)

    frame.start_row = start_row
    frame.end_row = start_row + length - 1

    # create the request object
    request = self.__dialect.batchUpdate(
      spreadsheetId=self.__handler.spreadsheet_id,
      body=dict(
        requests=[
          dict(
            deleteRange=dict(
              range=frame.grid_range,
              shiftDimension=DEFAULT_SHIFT_DIMENSION
            )
          )
        ]
      )
    )

    # apply dry_run mode
    if self.__dry_run_mode(options):
      return self.__dry_run_info(frame)

    # execute the request
    return dict(info=request.execute())


  def __dry_run_mode(self, options):
    return options.get('dry_run', False)


  def __dry_run_info(self, frame):
    return dict(dry_run=dict(
        spreadsheetId=self.__handler.spreadsheet_id,
        sheetId=self.sheet_id,
        sheetName=self.sheet_name,
        range=frame.human_readable
      )
    )


  def __newFrame(self, frame_range, field_mappings=dict()):
    return Frame(sheet=self, frame_range=frame_range, field_mappings=field_mappings)


  @property
  def __dialect(self):
    return self.__handler._dialect


class Frame(object):

  def __init__(self, **kwargs):
    self.__sheet = kwargs['sheet'] if 'sheet' in kwargs else None
    assert isinstance(self.__sheet, Sheet), 'sheet must be a Sheet instance'

    frame_range = kwargs['frame_range'] if 'frame_range' in kwargs else None
    assert isinstance(frame_range, dict), 'frame_range must be a dictionary'

    self.__left_col = frame_range['left_col']
    self.__left_col_index = lookup_number_of_colname(self.__left_col)

    self.__right_col = frame_range['right_col']
    self.__right_col_index = lookup_number_of_colname(self.__right_col)

    # determines the begin_row
    self.__begin_row = frame_range['begin_row']
    assert isinstance(self.__begin_row, int) and self.__begin_row > 0,\
        'begin_row must be a positive integer'

    # determines the first_row
    self.__first_row = self.__begin_row

    # determines the last_row (deprecated)
    self.__last_row = frame_range['last_row'] if 'last_row' in frame_range else None

    assert self.__last_row is None or (isinstance(self.__last_row, int) and self.__last_row > 0),\
        'last_row must be a positive integer or None'

    assert self.__last_row is None or self.__last_row >= self.__first_row,\
        'last_row must be equal or greater than the first_row'

    self.__skip = 0
    self.__limit = 0

    # init the start_row and end_row
    if 'start_row' in frame_range and isinstance(frame_range['start_row'], int):
      self.start_row = frame_range['start_row']

    if 'end_row' in frame_range and isinstance(frame_range['end_row'], int):
      self.end_row = frame_range['end_row']

    # determines the field_mappings
    self.field_mappings = kwargs['field_mappings']
    assert isinstance(self.field_mappings, dict)

    # create the mappings from the field_mappings settings
    self.__colnames = []
    self.__colalias = []
    for number in range(self.__left_col_index, self.__right_col_index + 1):
      _colname = lookup_colname_by_number(number)
      self.__colnames.append(_colname)
      self.__colalias.append(lookup_fieldname_from_mappings(_colname, self.field_mappings))

  @property
  def skip(self):
    return self.__skip

  @skip.setter
  def skip(self, value):
    assert isinstance(value, int) and value >=0, 'skip value must be a non-negative integer'
    self.__skip = value

  @property
  def limit(self):
    return self.__limit

  @limit.setter
  def limit(self, value):
    assert isinstance(value, int) and value >=0, 'limit value must be a non-negative integer'
    self.__limit = value

  @property
  def start_row(self):
    return self.__first_row if (self.__skip is None or self.__skip <= 0) else self.__first_row + self.__skip

  @start_row.setter
  def start_row(self, value):
    assert isinstance(value, int) and value >= self.__first_row,\
        'start_row must be equal or greater than the first_row'
    self.__skip = value - self.__first_row

  @property
  def end_row(self):
    _start_row = self.start_row
    _end_row = self.__last_row if self.__last_row is not None else None
    if self.__limit is not None and self.__limit > 0:
      if _end_row is None or _start_row + self.__limit <= _end_row:
        _end_row = _start_row + self.__limit - 1
    return _end_row

  @end_row.setter
  def end_row(self, value):
    assert isinstance(value, int) and value >=0, 'end_row value must be a non-negative integer'
    assert value >= self.start_row, 'end_row must be equal or greater than the start_row'
    self.__limit = value - self.start_row + 1

  @property
  def a1_range(self):
    _start_row = self.start_row
    _end_row = self.end_row

    rangeSpec = self.__sheet.sheet_name + '!' + self.__left_col + str(_start_row) + ':' + self.__right_col
    if _end_row is not None:
      rangeSpec = rangeSpec + str(_end_row)

    return rangeSpec

  @property
  def grid_range(self):
    _end_row = self.end_row
    if not isinstance(_end_row, int):
      raise InvalidGridRangeError('end_row must be determined as a positive integer')
    return dict(
      sheetId=self.__sheet.sheet_id,
      startColumnIndex=self.__left_col_index,
      endColumnIndex=self.__right_col_index + 1,
      startRowIndex=(self.start_row - 1),
      endRowIndex=(_end_row - 1) + 1,
    )

  @property
  def human_readable(self):
    return dict(
      leftColumn=self.__left_col,
      rightColumn=self.__right_col,
      startRow=self.start_row,
      endRow=self.end_row,
    )

  @property
  def without_bottom(self):
    copied = copy.copy(self)
    copied.__last_row = None
    copied.skip = 0
    copied.limit = 0
    return copied

  def convert_records_to_rows(self, records, includes=None, excludes=None):
    has_includes = (includes is not None) and (len(includes) > 0)
    has_excludes = (excludes is not None) and (len(excludes) > 0)
    # transform the records
    values = []
    for jsonobj in records:
      if 'record' in jsonobj:
        record = jsonobj['record']

        row = []
        for number in range(self.__right_col_index - self.__left_col_index + 1):
          # check the colalias
          fieldname = self.__colalias[number]
          if fieldname in record:
            if self.__satisfy(has_includes, includes, has_excludes, excludes, fieldname):
              row.append(record[fieldname])
            else:
              row.append(None)
            continue
          # check the colname
          fieldname = self.__colnames[number]
          if fieldname in record:
            if self.__satisfy(has_includes, includes, has_excludes, excludes, fieldname):
              row.append(record[fieldname])
            else:
              row.append(None)
            continue
          # not found
          row.append(None)

        if len(row) > 0:
          values.append(row)
    return values

  def convert_rows_to_records(self, values, includes=None, excludes=None):
    has_includes = (includes is not None) and (len(includes) > 0)
    has_excludes = (excludes is not None) and (len(excludes) > 0)
    datalist = []
    if values is not None:
      for row in values:
        _len_row = len(row)
        record = dict()
        for ind in range(self.__right_col_index - self.__left_col_index + 1):
          fieldname = self.__colalias[ind]
          if self.__satisfy(has_includes, includes, has_excludes, excludes, fieldname):
            if ind >= _len_row:
              record[fieldname] = None
              continue
            record[fieldname] = row[ind]
        datalist.append(record)
    return datalist

  def __satisfy(self, has_includes, includes, has_excludes, excludes, fieldname):
    if not has_excludes or (fieldname not in excludes):
      if not has_includes or (fieldname in includes):
        return True
    return False
