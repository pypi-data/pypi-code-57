import re
from abc import ABC
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

import fitz

PathLike = Union[Path, str]


def highlight(file_path: PathLike, out: Optional[PathLike] = None):
    file_path = Path(file_path)
    count = 0
    doc = fitz.open(file_path)
    try:
        for i in range(doc.pageCount):
            page = doc.loadPage(i)
            count += _highlight_page(page)
        out = _generate_out_path(out, file_path, count)
        doc.save(str(out))
        return out, count
    finally:
        doc.close()


def _highlight_page(p):
    count = 0
    words = list(map(Text, p.getTextWords()))
    for i, v in enumerate(words):
        if rule.check(i, v, words):
            count += 1
            rect = fitz.Rect(v.location)
            annot = p.addHighlightAnnot(rect)
            color = annot.colors
            color['stroke'][:2] = 0.0, 0.0
            annot.setColors(color)
            annot.setOpacity(0.2)
            annot.update()
    return count


def _generate_out_path(out: Optional[PathLike], file_path: Path, count) -> Path:
    if out is None:
        filename = file_path.name
        time = datetime.now().strftime('%Y.%m.%d.%H%M')
        new_name = f'[highlighted.{count}][{time}] {filename}'
        return file_path.with_name(new_name)
    else:
        return Path(out)


class Text:

    def __init__(self, data):
        self.word: str = data[4]
        self.location = data[:4]


class AbstractRule(ABC):

    def check(self, index: int, word: Text, words: List[Text]) -> bool:
        raise NotImplementedError


class DefaultRule(AbstractRule):

    def __init__(self):
        self.pattern_prev = re.compile(r'.*[.?!](\d+|\)|”)*')
        self.pattern_this = re.compile(r'[A-Z].*')

    def check(self, index: int, word: Text, words: List[Text]) -> bool:
        if index == 0:
            return False
        return self._check(words[index-1], word)

    def _check(self, word_prev: Text, word_this: Text):
        prev, this = word_prev.word, word_this.word
        return self._check_prev(prev) and self._check_this(this)

    def _check_prev(self, word: str):
        """检查前一个单词是否是句尾"""
        return self.pattern_prev.fullmatch(word)

    def _check_this(self, word: str):
        """检查目标单词是否是句首
        必要性：解决类似 e.g. 的问题
        局限性：类似 "PET" 或 "fMRI" 的句首无法解决
        """
        while word and word[0] in ['(', '“']:
            word = word[1:]
        return self.pattern_this.fullmatch(word) and any([
            word.istitle(),
            word.split('’')[0].istitle(),
            word.split("'")[0].istitle(),
            word.split('-')[0].istitle(),
            word.split(chr(8208))[0].istitle(),
        ])


rule: AbstractRule = DefaultRule()


def set_rule(custom_rule):
    if not isinstance(custom_rule, AbstractRule):
        raise TypeError('rule should be subclass of AbstractRule')
    global rule
    rule = custom_rule
