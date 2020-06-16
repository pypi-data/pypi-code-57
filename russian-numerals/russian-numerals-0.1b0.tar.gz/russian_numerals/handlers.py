# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#

from __future__ import unicode_literals

import re
from decimal import Decimal
from six import ensure_text, string_types


class NumberToWords:
    """
    Переводит дробное или целое число в количественные числительные
    без указания единиц измерения.
    """
    words0 = (1, '', '', '')
    words1 = (1, '', '', '', 3)

    def __init__(self, words_map=None):
        if words_map:
            self.words0, self.words1 = words_map

        # Проверка для наследуемых классов.
        assert isinstance(self.words0[0], int)
        assert isinstance(self.words0[1], string_types)
        assert isinstance(self.words0[2], string_types)
        assert isinstance(self.words0[3], string_types)
        assert isinstance(self.words1[0], int)
        assert isinstance(self.words1[1], string_types)
        assert isinstance(self.words1[2], string_types)
        assert isinstance(self.words1[3], string_types)
        assert isinstance(self.words1[4], int)

        self.numbers0 = (
            '',
            ('один', 'одна', 'одно'),
            ('два', 'две', 'два'),
            'три',
            'четыре',
            'пять',
            'шесть',
            'семь',
            'восемь',
            'девять',
        )
        self.numbers11 = (
            'десять',
            'одиннадцать',
            'двенадцать',
            'тринадцать',
            'четырнадцать',
            'пятнадцать',
            'шестнадцать',
            'семнадцать',
            'восемнадцать',
            'девятнадцать',
        )

        self.numbers10 = [
            '',
            'десять',
            'двадцать',
            'тридцать',
            'сорок',
            'пятьдесят',
            'шестьдесят',
            'семьдесят',
            'восемьдесят',
            'девяносто',
        ]

        self.numbers100 = [
            '',
            'сто',
            'двести',
            'триста',
            'четыреста',
            'пятьсот',
            'шестьсот',
            'семьсот',
            'восемьсот',
            'девятьсот',
        ]

        self.DIGITAL_WORDS = [
            [2, 'тысяча', 'тысячи', 'тысяч'],
            [1, 'миллион', 'миллиона', 'миллионов'],
            [1, 'миллиард', 'миллиарда', 'миллиардов'],
            [1, 'триллион', 'триллиона', 'триллионов'],
            [1, 'квадриллион', 'квадриллиона', 'квадриллионов'],
            [1, 'квинтиллион', 'квинтиллиона', 'квинтиллионов'],
            [1, 'секстиллион', 'секстиллиона', 'секстиллионов'],
            [1, 'септиллион', 'септиллиона', 'септиллионов'],
            [1, 'октиллион', 'октиллиона', 'октиллионов'],
            [1, 'нониллион', 'нониллиона', 'нониллионов'],
            [1, 'дециллион', 'дециллиона', 'дециллионов'],
        ]

    def morph(self, value, words):
        # value = '121343', words = [2, 'штука', 'штуки', 'штук']
        if not value:
            return
        if len(value) < 3:
            value = ('000%s' % value)[-3:]
        pre = int(value[-2:-1])
        last = int(value[-1])
        if last < 1 or pre == 1:
            return words[3]
        elif last < 2:
            return words[1]
        elif last < 5:
            return words[2]
        return words[3]

    def parse(self, value, words):
        s = '%d' % int(value)
        s = '0' * (3 - len(s) % 3) + s
        triples = [''.join(x) for x in zip(*[iter(s)] * 3)]

        result = []
        length = len(triples)
        all_words = [words] + self.DIGITAL_WORDS

        for i, part in enumerate(triples):
            if part == '000':
                continue

            words_row = all_words[length - i - 1]

            x = self.numbers100[int(part[0])]
            if x:
                result.append(x)

            if part[1] == '1':
                result.append(self.numbers11[int(part[2])])
            else:
                if part[1] != '0':
                    result.append(self.numbers10[int(part[1])])
                x = self.numbers0[int(part[2])]
                if x and not isinstance(x, string_types):
                    x = x[words_row[0] - 1]
                result.append(x)

            result.append(self.morph(part, words_row))

        return ' '.join(result)

    def prepare(self, value):
        if isinstance(value, (Decimal, int)):
            value = str(value)
            if 'E' in value:
                raise ValueError(
                    'Decimal value contains the Exponent: %s' % value
                )
        elif isinstance(value, float):
            # Учитывая особенности float в Python:
            # '%f' % 999999999999999.9 => '999999999999999.875000'
            # '%f' % 999999999999999.99 => '1000000000000000.000000'
            if value > 999999999999999.9:
                raise ValueError(
                    'Float value must be less than 999999999999999.9 '
                    'or use Decimal value.'
                )
            value = '%f' % value

        strings = ensure_text(value).split('.')[:2]
        if len(strings) == 1:
            strings.append('')
        elif strings[1]:
            count = self.words1[4]
            strings[1] = (strings[1] + ('0' * count))[:count]

        result = [self.parse(strings[0], self.words0)]
        if strings[1]:
            result.append(self.parse(strings[1], self.words1))

        return re.sub(r'\s+', ' ', ' '.join(result)).strip()


class NumberToRoubles(NumberToWords):
    """
    Переводит дробное или целое число в количественные числительные
    с рублями и копейками в качестве единиц измерения.
    """
    words0 = (1, 'рубль', 'рубля', 'рублей')
    words1 = (2, 'копейка', 'копейки', 'копеек', 2)


class NumberToTons(NumberToWords):
    """
    Переводит дробное или целое число в количественные числительные
    с тоннами и килограммами в качестве единиц измерения.
    """
    words0 = (2, 'тонна', 'тонны', 'тонн')
    words1 = (1, 'килограмм', 'килограмма', 'килограммов', 3)


class NumberToKilograms(NumberToWords):
    """
    Переводит дробное или целое число в количественные числительные
    с килограммами и граммами в качестве единиц измерения.
    """
    words0 = (1, 'килограмм', 'килограмма', 'килограммов')
    words1 = (1, 'грамм', 'грамма', 'граммов', 3)


class TextToNumbers:
    """
    Переводит найденные в тексте количественные числительные в числа.
    """

    def __init__(self):
        # Числа, после которых либо идёт слово "тысяча" (и далее),
        # либо это конец числительного.
        self.numbers0 = {
            'ноль': 0,
            'один': 1, 'одна': 1, 'одно': 1,
            'два': 2, 'две': 2, 'два': 2,
            'три': 3,
            'четыре': 4,
            'пять': 5,
            'шесть': 6,
            'семь': 7,
            'восемь': 8,
            'девять': 9,
        }
        # Числа, после которых либо идёт слово "тысяча" (и далее),
        # либо это конец числительного.
        self.numbers1 = {
            'десять': 10,
            'одиннадцать': 11,
            'двенадцать': 12,
            'тринадцать': 13,
            'четырнадцать': 14,
            'пятнадцать': 15,
            'шестнадцать': 16,
            'семнадцать': 17,
            'восемнадцать': 18,
            'девятнадцать': 19,
        }
        # Группа чисел, которые либо...
        self.numbers2 = {
            'двадцать': 20,
            'тридцать': 30,
            'сорок': 40,
            'пятьдесят': 50,
            'шестьдесят': 60,
            'семьдесят': 70,
            'восемьдесят': 80,
            'девяносто': 90,
        }
        self.numbers3 = {
            'сто': 100,
            'двести': 200,
            'триста': 300,
            'четыреста': 400,
            'пятьсот': 500,
            'шестьсот': 600,
            'семьсот': 700,
            'восемьсот': 800,
            'девятьсот': 900,
        }
        self.power_numbers = {
            'тысяча': 3, 'тысячи': 3, 'тысяч': 3,
            'миллион': 6, 'миллиона': 6, 'миллионов': 6,
            'миллиард': 9, 'миллиарда': 9, 'миллиардов': 9,
            'триллион': 12, 'триллиона': 12, 'триллионов': 12,
            'квадриллион': 15, 'квадриллиона': 15, 'квадриллионов': 15,
            'квинтиллион': 18, 'квинтиллиона': 18, 'квинтиллионов': 18,
            'секстиллион': 21, 'секстиллиона': 21, 'секстиллионов': 21,
            'септиллион': 24, 'септиллиона': 24, 'септиллионов': 24,
            'октиллион': 27, 'октиллиона': 27, 'октиллионов': 27,
            'нониллион': 30, 'нониллиона': 30, 'нониллионов': 30,
            'дециллион': 33, 'дециллиона': 33, 'дециллионов': 33,
        }
        self.all_words = {}
        self.all_words.update(self.numbers0)
        self.all_words.update(self.numbers1)
        self.all_words.update(self.numbers2)
        self.all_words.update(self.numbers3)
        self.all_words.update(self.power_numbers)

    def prepare(self, value):
        if not isinstance(value, string_types):
            value = str(value)
        value = ensure_text(value)
        source_words = [w for w in value.split(' ') if w]
        sections = (self.numbers0, self.numbers1, self.numbers2, self.numbers3,
                    self.power_numbers)
        # Сначала разбиваем строку на группы слов, где каждая группа - это
        # либо подряд идущие обычные слова (не числительные),
        # либо количественные числительные, принадлежащие одной величине.
        groups = []
        group = None
        for_digit = False
        for word in source_words:
            _word = word.lower()
            is_digit = _word in self.all_words
            if not group or for_digit != is_digit:
                group = [_word if is_digit else word]
                for_digit = is_digit
                groups.append([group, for_digit])
                continue
            elif not is_digit:
                group.append(word)
                continue

            prev = group[-1]

            # Числительные не могут быть из одной и той же секции.
            found = False
            for section in sections:
                if prev in section and _word in section:
                    group = [_word]
                    groups.append([group, for_digit])
                    found = True
                    break
            if found:
                continue
            # Когда за единицами или десятком не следует тысячи, то
            # это новое число.
            end_digit = prev in self.numbers0 or prev in self.numbers1
            if end_digit and _word not in self.power_numbers:
                group = [_word]
                groups.append([group, for_digit])
                continue
            # Перечисление десятков, а за ними сотен - это тоже новые числа.
            if prev in self.numbers2 and _word in self.numbers3:
                group = [_word]
                groups.append([group, for_digit])
                continue
            # Слово принадлежит текущему числительному.
            group.append(_word)

        result = []
        # Теперь преобразовываем количественные числительные в числа.
        for group, for_digit in groups:
            if not for_digit:
                result.extend(group)
                continue
            total = 0
            temp = 1 if group[0] in self.power_numbers else 0
            for number in group:
                if number in self.power_numbers:
                    total += temp * (10 ** self.power_numbers[number])
                    temp = 0
                else:
                    temp += self.all_words[number]
            total += temp
            result.append('%d' % total)

        return re.sub(r'\s+', ' ', ' '.join(result)).strip()
