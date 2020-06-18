from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg


class AbbreviationNumberConversor(NormalizerBase):
    NAME = "abbreviation_number_conversor_norm"
    DESCRIPTION_TRAINING = """
    """
    DESCRIPTION_DECODING = """
          Replace number abbrevations between english, french and spanish.
    """

    class Replacement:
        def __init__(self, desired: str, expected: str):
            self.pairs = {
                expected: desired,
                expected.capitalize(): desired.capitalize()
            }

        def replace(self, text: str):
            for key, value in self.pairs.items():
                text = text.replace(key, value)
            return text

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        super().__init__(src_lang, tgt_lang)
        if self.tgt_lang == "es":
            if self.src_lang == "fr":
                self.replacements = [
                    self.Replacement('nº', 'n.o.')
                ]
            if self.src_lang == "en":
                self.replacements = [
                    self.Replacement('nº', 'no.')
                ]
        elif self.tgt_lang == "fr":
            if self.src_lang == "es":
                self.replacements = [
                    self.Replacement('n.o.', 'nº' )
                ]
            if self.src_lang == "en":
                self.replacements = [
                    self.Replacement('n.o.', 'no.')
                ]
        elif self.tgt_lang == "en":
            if self.src_lang == "fr":
                self.replacements = [
                    self.Replacement('no.', 'n.o.')
                ]
            if self.src_lang == "es":
                self.replacements = [
                    self.Replacement('no.', 'nº')
                ]

    def apply_replacements(self, text: str):
        for replacement in self.replacements:
            text = replacement.replace(text)
        return text

    def process_train(self, seg: Seg) -> None:
        if seg.src != "" and seg.src != "\n":
            if self.src_lang == "en":
                for key, value in self.replacements[0].pairs.items():
                    index = seg.tgt.find(key)
                    if index > -1 and index + 4 < len(seg.tgt):
                        if seg.tgt[index+4].isnumeric():
                            seg.tgt = self.apply_replacements(seg.tgt)
            elif self.src_lang in ['es','fr']:
                for key, value in self.replacements[0].pairs.items():
                    index = seg.tgt.find(key)
                    if index > -1:
                        seg.tgt = self.apply_replacements(seg.tgt)

    def process_src_decoding(self, seg: Seg) -> None:
        pass

    def process_tgt_decoding(self, seg: Seg) -> None:
        pass
