from despeech import DeSpeechConverter


class TestConverter:
    def test_ich(self):
        converter = DeSpeechConverter()
        text = 'Er brummte:"Ich gehe in die Bierstube".'
        result = converter.convert(text)
        assert result == 'er brummte, er geht in die bierstube.'

    def test_du(self):
        converter = DeSpeechConverter()
        text = 'Er sagte:"Du sollst es shaffen".'
        result = converter.convert(text)
        assert result == 'er sagte, ich soll es shaffen.'

    def test_sie(self):
        converter = DeSpeechConverter()
        text = 'die lehrerin sagte:"ich liebe".'
        result = converter.convert(text)
        assert result == 'die lehrerin sagte, sie liebt.'
