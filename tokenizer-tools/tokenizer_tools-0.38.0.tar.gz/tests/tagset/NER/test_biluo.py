from tokenizer_tools.tagset.NER.BILUO import BILUOEncoderDecoder, BILUOSequenceEncoderDecoder

def test_generate_tag():
    a = BILUOEncoderDecoder("B")
    #a.tag_name = 'B'
    b = BILUOEncoderDecoder.generate_tag(a, "c")
    assert 'c-B' == b

    a = BILUOEncoderDecoder(None)
    c = BILUOEncoderDecoder.generate_tag(a, "B")
    assert 'B' == c

    d = BILUOEncoderDecoder("O")
    e = BILUOEncoderDecoder.generate_tag(d, "1")
    assert 'O' == e

#todo Does this sequence is retative to that sequence?
def test_encode():
    a = BILUOEncoderDecoder(None)
    sequence = 'my dream will come true'
    s = BILUOEncoderDecoder.encode(a, sequence);
    assert len(s) == 23

    b = BILUOEncoderDecoder('B')
    sequence = 'ha'
    s = BILUOEncoderDecoder.encode(b, sequence);
    assert ['B-B', 'L-B'] == s

    c = BILUOEncoderDecoder('aa')
    sequence = 'y'
    s = BILUOEncoderDecoder.encode(c, sequence);
    assert ['U-aa'] == s

def test_all_tag_set():
    a = BILUOEncoderDecoder('F')
    result = BILUOEncoderDecoder.all_tag_set(a)
    assert len(result) == 5

def test_parse_tag():
    a = BILUOSequenceEncoderDecoder()
    b = BILUOSequenceEncoderDecoder.parse_tag(a, 'O')
    assert 'O',None == b

    c = BILUOSequenceEncoderDecoder()
    d = BILUOSequenceEncoderDecoder.parse_tag(a, 'B-I')
    assert 'B', 'I' == d

    e = BILUOSequenceEncoderDecoder()
    try:
        f = BILUOSequenceEncoderDecoder.parse_tag(a, 'H-Z')
    except Exception as e:
        assert True == isinstance(e, ValueError)

def test_is_prefix_legal():
    a = BILUOSequenceEncoderDecoder()
    b = BILUOSequenceEncoderDecoder.is_prefix_legal(a, 'B', 'I')
    assert True == b

    c = BILUOSequenceEncoderDecoder()
    d = BILUOSequenceEncoderDecoder.is_prefix_legal(c, 'F', 'G')
    assert False == d

def test_decode_to_offset():
    sequence = ['B-L']
    s = BILUOSequenceEncoderDecoder()
    rs = BILUOSequenceEncoderDecoder.decode_to_offset(s, sequence)
    assert len(rs) == 0

#TODO need to fix it
def test_to_offset():
    s = BILUOSequenceEncoderDecoder()
    rs = BILUOSequenceEncoderDecoder.to_offset(s, ['B-I'], 'sadines')
    print(rs)






