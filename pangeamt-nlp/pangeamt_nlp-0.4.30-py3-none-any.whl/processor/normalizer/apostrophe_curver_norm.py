from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg


class ApostropheCurverNorm(NormalizerBase):

    NAME = "apostrophe_curver_norm"

    DESCRIPTION_TRAINING = """
        Replaces all uncurved apostrophes (') with curved apostrophes (’). Note: also affects straight quotes 
        (same symbol)
    """

    DESCRIPTION_DECODING = """
        Replaces all uncurved apostrophes (') with curved apostrophes (’) in the src. Leaves target unchanged.
    """

    def __init__(self, src_lang, tgt_lang):
        super().__init__(src_lang, tgt_lang)
        self.in_char = "'"
        self.out_char = "’"

    def _normalize(self, text):
        res_text = []
        for char in text:
            if char == self.in_char:
                res_text.append(self.out_char)
            else:
                res_text.append(char)
        return "".join(res_text)

    # Called when training
    def process_train(self, seg: Seg) -> None:
        seg.src = self._normalize(seg.src)
        if seg.tgt is not None:
            seg.tgt = self._normalize(seg.tgt)

    # Called when using model (before calling model to translate)
    def process_src_decoding(self, seg: Seg) -> None:
        seg.src = self._normalize(seg.src)

    # Called after the model translated (in case this would be necessary; usually not the case)
    def process_tgt_decoding(self, seg: Seg) -> None:
        pass
