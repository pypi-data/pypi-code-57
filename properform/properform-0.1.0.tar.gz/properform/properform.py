# -*- coding: utf-8 -*-
# Copyright 2017 - 2019 ibelie, Chen Jie, Joungtao. All rights reserved.
# Use of this source code is governed by The MIT License
# that can be found in the LICENSE file.

from __future__ import print_function

import os
import sys
import json
import struct
import marshal

if sys.version_info[0] == 3:
	from urllib.parse import quote
	from urllib.request import Request, urlopen
	from io import BytesIO
else:
	from urllib import quote
	from urllib2 import Request, urlopen
	from cStringIO import StringIO as BytesIO


PROFILE_NAMESET_LEN = '!I'
PROFILE_NAMESET_ITEM = '!H'
PROFILE_CALLEE_LEN = '!I'
PROFILE_CALLEE_ITEM = '!IIIIIddI'
PROFILE_CALLER_ITEM = '!IIIIIdd'

def serialize_profile(writer, stats):
	nameset = set()
	for (f, l, n), (pc, rc, it, ct, callers) in stats.items():
		nameset.add(f)
		nameset.add(n)
		for (f, l, n), (pc, rc, it, ct) in callers.items():
			nameset.add(f)
			nameset.add(n)

	writer.write(struct.pack(PROFILE_NAMESET_LEN, len(nameset)))
	names = {}
	for name in nameset:
		s = name if isinstance(name, type(b'')) else name.encode('utf-8', 'replace')
		writer.write(struct.pack(PROFILE_NAMESET_ITEM, len(s)))
		writer.write(s)
		names[name] = len(names)

	writer.write(struct.pack(PROFILE_CALLEE_LEN, len(stats)))
	for (f, l, n), (pc, rc, it, ct, callers) in stats.items():
		writer.write(struct.pack(PROFILE_CALLEE_ITEM, names[f], l, names[n], pc, rc, it, ct, len(callers)))
		for (f, l, n), (pc, rc, it, ct) in callers.items():
			writer.write(struct.pack(PROFILE_CALLER_ITEM, names[f], l, names[n], pc, rc, it, ct))

def deserialize_profile(reader):
	names = []
	name_count, = struct.unpack(PROFILE_NAMESET_LEN, reader.read(struct.calcsize(PROFILE_NAMESET_LEN)))
	for _ in range(name_count):
		size, = struct.unpack(PROFILE_NAMESET_ITEM, reader.read(struct.calcsize(PROFILE_NAMESET_ITEM)))
		name = reader.read(size)
		name = name if isinstance(name, str) else name.decode('utf-8')
		names.append(name)

	stats = {}
	stat_count, = struct.unpack(PROFILE_CALLEE_LEN, reader.read(struct.calcsize(PROFILE_CALLEE_LEN)))
	for _ in range(stat_count):
		f, l, n, pc, rc, it, ct, caller_count = struct.unpack(PROFILE_CALLEE_ITEM, reader.read(struct.calcsize(PROFILE_CALLEE_ITEM)))
		callers = {}
		stats[(names[f], l, names[n])] = (pc, rc, it, ct, callers)
		for _ in range(caller_count):
			f, l, n, pc, rc, it, ct = struct.unpack(PROFILE_CALLER_ITEM, reader.read(struct.calcsize(PROFILE_CALLER_ITEM)))
			callers[(names[f], l, names[n])] = (pc, rc, it, ct)

	return stats


MEMLEAK_STRINGSET_LEN = '!I'
MEMLEAK_STRINGSET_ITEM = '!H'
MEMLEAK_OBJECT_LEN = '!I'
MEMLEAK_OBJECT_ITEM = '!QIIIII'
MEMLEAK_REFERENCE_ITEM = '!Q'

def serialize_memleak(writer, memleak):
	stringset = set()
	for t, v, f, n, rs in memleak.values():
		stringset.add(t)
		stringset.add(v)
		stringset.add(f)

	writer.write(struct.pack(MEMLEAK_STRINGSET_LEN, len(stringset)))
	strings = {}
	for ss in stringset:
		s = ss if isinstance(ss, type(b'')) else ss.encode('utf-8', 'replace')
		writer.write(struct.pack(MEMLEAK_STRINGSET_ITEM, len(s)))
		writer.write(s)
		strings[ss] = len(strings)

	writer.write(struct.pack(MEMLEAK_OBJECT_LEN, len(memleak)))
	for i, (t, v, f, n, rs) in memleak.items():
		writer.write(struct.pack(MEMLEAK_OBJECT_ITEM, int(i), strings[t], strings[v], strings[f], n, len(rs)))
		for r in rs:
			writer.write(struct.pack(MEMLEAK_REFERENCE_ITEM, r))

def deserialize_memleak(reader):
	strings = []
	string_count, = struct.unpack(MEMLEAK_STRINGSET_LEN, reader.read(struct.calcsize(MEMLEAK_STRINGSET_LEN)))
	for _ in range(string_count):
		size, = struct.unpack(MEMLEAK_STRINGSET_ITEM, reader.read(struct.calcsize(MEMLEAK_STRINGSET_ITEM)))
		s = reader.read(size)
		s = s if isinstance(s, str) else s.decode('utf-8')
		strings.append(s)

	memleak = {}
	memleak_count, = struct.unpack(MEMLEAK_OBJECT_LEN, reader.read(struct.calcsize(MEMLEAK_OBJECT_LEN)))
	for _ in range(memleak_count):
		i, t, v, f, n, rs_count = struct.unpack(MEMLEAK_OBJECT_ITEM, reader.read(struct.calcsize(MEMLEAK_OBJECT_ITEM)))
		rs = []
		memleak[i] = (strings[t], strings[v], strings[f], n, rs)
		for _ in range(rs_count):
			r, = struct.unpack(MEMLEAK_REFERENCE_ITEM, reader.read(struct.calcsize(MEMLEAK_REFERENCE_ITEM)))
			rs.append(r)

	return memleak


DATA_TYPE_PROFILE = 1
DATA_TYPE_MEMLEAK = 2
DATA_TYPE_HEADER = '!H'

class DataFormatException(BaseException):
	pass

def Iterate(reader):
	header = reader.read(struct.calcsize(DATA_TYPE_HEADER))
	while header:
		t, = struct.unpack(DATA_TYPE_HEADER, header)
		if t == DATA_TYPE_PROFILE:
			yield t, deserialize_profile(reader)
		elif t == DATA_TYPE_MEMLEAK:
			yield t, deserialize_memleak(reader)
		else:
			raise DataFormatException()
		header = reader.read(struct.calcsize(DATA_TYPE_HEADER))

def Push(url, token, project, commit, profile = '', memleak = '', tag = 'default'):
	assert profile or memleak
	data = BytesIO()
	if os.path.isfile(profile):
		with open(profile, 'rb') as f:
			data.write(struct.pack(DATA_TYPE_HEADER, DATA_TYPE_PROFILE))
			serialize_profile(data, marshal.load(f))
	if os.path.isfile(memleak):
		with open(memleak, 'rb') as f:
			data.write(struct.pack(DATA_TYPE_HEADER, DATA_TYPE_MEMLEAK))
			serialize_memleak(data, json.load(f))

	if not url.startswith('http'):
		url = 'http://' + url
	request = Request('%(url)s?token=%(token)s&project=%(project)s&commit=%(commit)s&tag=%(tag)s' % {
		'url': url,
		'token': token,
		'project': project,
		'commit': commit,
		'tag': quote(tag),
	}, data.getvalue())
	response = json.load(urlopen(request))
	if not response['error']:
		print('[Properform] Push Success!')
	else:
		print('[Properform] Push Error: %(error)s!' % response)

def Convert(dst, src):
	with open(src, 'rb') as s:
		for t, stats in Iterate(s):
			if t == DATA_TYPE_PROFILE:
				with open(dst, 'wb') as d:
					marshal.dump(stats, d)
				break
