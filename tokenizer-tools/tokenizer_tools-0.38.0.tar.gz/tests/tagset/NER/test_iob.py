from tokenizer_tools.tagset.NER.IOB import IobEncoderDecoder, IobSequenceEncoderDecoder

def test_generate_tag():
    s = IobEncoderDecoder("B")
    rs = IobEncoderDecoder.generate_tag(s, "S")
    print(rs)
    assert 'S-B' == rs

def test_encode():
    sequence = 'hero'
    s = IobEncoderDecoder("D")
    rs = IobEncoderDecoder.encode(s, sequence)
    print(rs)
    assert ['B-D', 'I-D', 'I-D', 'I-D'] == rs

def test_all_tag_set():
    s = IobEncoderDecoder("D")
    rs = IobEncoderDecoder.all_tag_set(s)
    print(rs)
    assert len(rs) == 3

def test_parse_tag():
    s = IobSequenceEncoderDecoder()
    rs = IobSequenceEncoderDecoder.parse_tag(s, 'B-I')
    print(rs)
    assert 'B', 'I' == rs

def test_is_prefix_legal():
    s = IobSequenceEncoderDecoder()
    rs = IobSequenceEncoderDecoder.is_prefix_legal(s, 'B', 'O')
    print(rs)
    assert True == rs

def test_decode_to_offset():
    s = IobSequenceEncoderDecoder()
    sequence = ['B-I', 'B-O']
    rs = IobSequenceEncoderDecoder.decode_to_offset(s, sequence)
    print(rs)
    assert [(0, 1, 'I'), (1, 2, 'O')] == rs

