# 3rd party
import pytest

# this package
import sd_ujson


# 2007-10-05
JSONDOCS = [
		# http://json.org/JSON_checker/test/fail1.json
		'"A JSON payload should be an object or array, not a string."',
		# http://json.org/JSON_checker/test/fail2.json
		'["Unclosed array"',
		# http://json.org/JSON_checker/test/fail3.json
		'{unquoted_key: "keys must be quoted"}',
		# http://json.org/JSON_checker/test/fail4.json
		# TODO: '["extra comma",]',
		# http://json.org/JSON_checker/test/fail5.json
		'["double extra comma",,]',
		# http://json.org/JSON_checker/test/fail6.json
		'[   , "<-- missing value"]',
		# http://json.org/JSON_checker/test/fail7.json
		'["Comma after the close"],',
		# http://json.org/JSON_checker/test/fail8.json
		'["Extra close"]]',
		# http://json.org/JSON_checker/test/fail9.json
		# TODO: '{"Extra comma": true,}',
		# http://json.org/JSON_checker/test/fail10.json
		'{"Extra value after close": true} "misplaced quoted value"',
		# http://json.org/JSON_checker/test/fail11.json
		'{"Illegal expression": 1 + 2}',
		# http://json.org/JSON_checker/test/fail12.json
		'{"Illegal invocation": alert()}',
		# http://json.org/JSON_checker/test/fail13.json
		# TODO: '{"Numbers cannot have leading zeroes": 013}',
		# http://json.org/JSON_checker/test/fail14.json
		'{"Numbers cannot be hex": 0x14}',
		# http://json.org/JSON_checker/test/fail15.json
		'["Illegal backslash escape: \\x15"]',
		# http://json.org/JSON_checker/test/fail16.json
		'[\\naked]',
		# http://json.org/JSON_checker/test/fail17.json
		'["Illegal backslash escape: \\017"]',
		# http://json.org/JSON_checker/test/fail18.json
		# TODO: '[[[[[[[[[[[[[[[[[[[["Too deep"]]]]]]]]]]]]]]]]]]]]',
		# http://json.org/JSON_checker/test/fail19.json
		'{"Missing colon" null}',
		# http://json.org/JSON_checker/test/fail20.json
		'{"Double colon":: null}',
		# http://json.org/JSON_checker/test/fail21.json
		'{"Comma instead of colon", null}',
		# http://json.org/JSON_checker/test/fail22.json
		'["Colon instead of comma": false]',
		# http://json.org/JSON_checker/test/fail23.json
		'["Bad value", truth]',
		# http://json.org/JSON_checker/test/fail24.json
		"['single quote']",
		# http://json.org/JSON_checker/test/fail25.json
		# TODO: '["\ttab\tcharacter\tin\tstring\t"]',
		# http://json.org/JSON_checker/test/fail26.json
		'["tab\\   character\\   in\\  string\\  "]',
		# http://json.org/JSON_checker/test/fail27.json
		# TODO: '["line\nbreak"]',
		# http://json.org/JSON_checker/test/fail28.json
		'["line\\\nbreak"]',
		# http://json.org/JSON_checker/test/fail29.json
		# TODO: '[0e]',
		# http://json.org/JSON_checker/test/fail30.json
		# TODO: '[0e+]',
		# http://json.org/JSON_checker/test/fail31.json
		'[0e+-1]',
		# http://json.org/JSON_checker/test/fail32.json
		'{"Comma instead if closing brace": true,',
		# http://json.org/JSON_checker/test/fail33.json
		'["mismatch"}',
		# http://code.google.com/p/simplejson/issues/detail?id=3
		# TODO: '["A\u001FZ control characters in string"]',
		]

SKIPS = {
		'"A JSON payload should be an object or array, not a string."': "why not have a string payload?",
		'[[[[[[[[[[[[[[[[[[[["Too deep"]]]]]]]]]]]]]]]]]]]]': "spec doesn't specify any nesting limitations",
		}


def test_failures():
	for idx, doc in enumerate(JSONDOCS):
		idx = idx + 1
		if doc in SKIPS:
			sd_ujson.loads(doc)
			continue
		try:
			sd_ujson.loads(doc)
		except ValueError:
			pass
		else:
			pytest.fail("Expected failure for fail{0}.json: {1!r}".format(idx, doc))


@pytest.mark.xfail
def test_non_string_keys_dict():
	import sys
	
	data = {'a': 1, (1, 2): 2}
	
	# TODO:
	if sys.version_info.major >= 3 and sys.version_info.minor > 6:
		match_string = "keys must be str, int, float, bool or None, not tuple"
	else:
		match_string = "keys must be a string"

	with pytest.raises(TypeError, match=match_string):
		sd_ujson.dumps(data)


@pytest.mark.xfail
def test_not_serializable():
	import sys
	with pytest.raises(TypeError, match="Object of type [']*module[']* is not JSON serializable"):
		sd_ujson.dumps(sys)


@pytest.mark.xfail
def test_truncated_input():
	test_cases = [
			('', 'Expecting value', 0),
			('[', 'Expecting value', 1),
			('[42', "Expecting ',' delimiter", 3),
			('[42,', 'Expecting value', 4),
			('["', 'Unterminated string starting at', 1),
			('["spam', 'Unterminated string starting at', 1),
			('["spam"', "Expecting ',' delimiter", 7),
			('["spam",', 'Expecting value', 8),
			('{', 'Expecting property name enclosed in double quotes', 1),
			('{"', 'Unterminated string starting at', 1),
			('{"spam', 'Unterminated string starting at', 1),
			('{"spam"', "Expecting ':' delimiter", 7),
			('{"spam":', 'Expecting value', 8),
			('{"spam":42', "Expecting ',' delimiter", 10),
			('{"spam":42,', 'Expecting property name enclosed in double quotes', 11),
			]
	test_cases += [
			('"', 'Unterminated string starting at', 0),
			('"spam', 'Unterminated string starting at', 0),
			]
	for data, msg, idx in test_cases:
		with pytest.raises(sd_ujson.JSONDecodeError) as err:
			sd_ujson.loads(data)
			
		assert err.value.msg == msg
		assert err.value.pos == idx
		assert err.value.lineno == 1
		assert err.value.colno == idx + 1
		assert str(err.value) == f'{msg}: line 1 column {idx + 1:d} (char {idx:d})'


@pytest.mark.xfail
def test_unexpected_data():
	test_cases = [
			('[,', 'Expecting value', 1),
			('{"spam":[}', 'Expecting value', 9),
			('[42:', "Expecting ',' delimiter", 3),
			('[42 "spam"', "Expecting ',' delimiter", 4),
			('[42,]', 'Expecting value', 4),
			('{"spam":[42}', "Expecting ',' delimiter", 11),
			('["]', 'Unterminated string starting at', 1),
			('["spam":', "Expecting ',' delimiter", 7),
			('["spam",]', 'Expecting value', 8),
			('{:', 'Expecting property name enclosed in double quotes', 1),
			('{,', 'Expecting property name enclosed in double quotes', 1),
			('{42', 'Expecting property name enclosed in double quotes', 1),
			('[{]', 'Expecting property name enclosed in double quotes', 2),
			('{"spam",', "Expecting ':' delimiter", 7),
			('{"spam"}', "Expecting ':' delimiter", 7),
			('[{"spam"]', "Expecting ':' delimiter", 8),
			('{"spam":}', 'Expecting value', 8),
			('[{"spam":]', 'Expecting value', 9),
			('{"spam":42 "ham"', "Expecting ',' delimiter", 11),
			('[{"spam":42]', "Expecting ',' delimiter", 11),
			('{"spam":42,}', 'Expecting property name enclosed in double quotes', 11),
			]
	for data, msg, idx in test_cases:
		with pytest.raises(sd_ujson.JSONDecodeError) as err:
			sd_ujson.loads(data)
		assert err.value.msg == msg
		assert err.value.pos == idx
		assert err.value.lineno == 1
		assert err.value.colno == idx + 1
		assert str(err.value) == f'{msg}: line 1 column {idx + 1:d} (char {idx:d})'


@pytest.mark.xfail
def test_extra_data():
	test_cases = [
			('[]]', 'Extra data', 2),
			('{}}', 'Extra data', 2),
			('[],[]', 'Extra data', 2),
			('{},{}', 'Extra data', 2),
			]
	test_cases += [
			('42,"spam"', 'Extra data', 2),
			('"spam",42', 'Extra data', 6),
			]
	for data, msg, idx in test_cases:
		with pytest.raises(sd_ujson.JSONDecodeError) as err:
			sd_ujson.loads(data)
			
		assert err.value.msg == msg
		assert err.value.pos == idx
		assert err.value.lineno == 1
		assert err.value.colno == idx + 1
		assert str(err.value) == f'{msg}: line 1 column {idx + 1:d} (char {idx:d})'


@pytest.mark.xfail
def test_linecol():
	test_cases = [
			('!', 1, 1, 0),
			(' !', 1, 2, 1),
			('\n!', 2, 1, 1),
			('\n  \n\n     !', 4, 6, 10),
			]
	for data, line, col, idx in test_cases:
		with pytest.raises(sd_ujson.JSONDecodeError) as err:
			sd_ujson.loads(data)

		assert err.value.msg == 'Expecting value'
		assert err.value.pos == idx
		assert err.value.lineno == line
		assert err.value.colno == col
		assert str(err.value) == f'Expecting value: line {line} column {col:d} (char {idx:d})'
