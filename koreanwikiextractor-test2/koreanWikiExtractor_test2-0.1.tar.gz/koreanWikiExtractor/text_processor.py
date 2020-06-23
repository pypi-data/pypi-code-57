# coding=utf-8

import mwparserfromhell
from bs4 import BeautifulSoup
import re


class TextProcessor(object):

    def __init__(self, texts, values=[]):
        self.__values = values
        self.__texts = texts

    def convert_mediawiki_to_plain_text(self):
        self.__texts = self._remove_templates(self.__texts)
        self.__texts = self._remove_header(self.__texts)
        self.__texts = self._remove_wikitable(self.__texts)
        self.__texts = self._remove_wikilinks2(self.__texts)
        self.__texts = self._remove_wikitable2(self.__texts)
        self.__texts = self._remove_externalLink(self.__texts)
        self.__texts = self._remove_extra(self.__texts)
        self.__texts = self._remove_html(self.__texts)

        return self.__texts


    # {{ }} wiki 문법 templeate을 제거
    def _remove_templates(self, docs):
        temp_docs = []
        for doc in docs:
            wikicode = mwparserfromhell.parse(doc)
            templates = wikicode.filter_templates()
            for template in templates:
                if template.name.lower() == 'lang' or template.name.lower() == 'llang':
                    if len(template.params) > 0:
                        doc = doc.replace(str(template), str(template.params[-1]))
                elif template.name.lower() == 'kor':
                    doc = doc.replace(str(template), '대한민국')
                elif template.name.lower() == 'jpn':
                    doc = doc.replace(str(template), '일본')
                elif template.name.lower() == 'sin':
                    doc = doc.replace(str(template), '싱가포르')
                elif template.name.lower() == 'usa':
                    doc = doc.replace(str(template), '미국')
                elif template.name.lower() == 'esp':
                    doc = doc.replace(str(template), '스페인')
                elif template.name.lower() == 'aus':
                    doc = doc.replace(str(template), '호주')
                elif template.name.lower() == 'irl':
                    doc = doc.replace(str(template), '아일랜드')
                elif template.name == '국기' or template.name == '국기나라' or template.name == '국기그림':
                    if len(template.params) > 0:
                        doc = doc.replace(str(template), str(template.params[-1]))
                elif template.name == '본명':
                    if len(template.params) > 0:
                        doc = doc.replace(str(template), str(template.params[-1]))
                elif template.name.lower() == 'ja-y' or template.name.lower() == 'ja-y2':
                    if len(template.params) > 0:
                        doc = doc.replace(str(template), str(template.params[-1]))
                elif template.name == '출생일과 나이' or template.name == '출생일과 만나이' or template.name == '출생일'\
                        or template.name == '사망일과 나이' or template.name == '사망일과 만나이' or template.name == '사망일':
                    if len(template.params) > 2:
                        s = str(template.params[0])+'년 '+str(template.params[1])+'월 '+str(template.params[2])+'일'
                        doc = doc.replace(str(template), str(s))
                elif template.name.lower() == '언어 이름':
                    if len(template.params) > 0:
                        if str(template.params[-1]) == 'ko':
                            doc = doc.replace(str(template), '한국어')
                        elif str(template.params[-1]) == 'en':
                            doc = doc.replace(str(template), '영어')
                        elif str(template.params[-1]) == 'ar':
                            doc = doc.replace(str(template), '아랍어')
                        elif str(template.params[-1]) == 'ja':
                            doc = doc.replace(str(template), '일본어')
                        elif str(template.params[-1]) == 'es':
                            doc = doc.replace(str(template), '스페인어')
                        elif str(template.params[-1]) == 'fr':
                            doc = doc.replace(str(template), '프랑스어')
                        elif str(template.params[-1]) == 'de':
                            doc = doc.replace(str(template), '독일어')
                else:
                    doc = doc.replace(str(template), '')
            temp_docs.append(doc)
        return temp_docs

    # === ===, == ==  wiki문법 header를 제거
    def _remove_header(self, docs):
        temp_docs = []
        for doc in docs:
            wikicode = mwparserfromhell.parse(doc)
            headings = wikicode.filter_headings()
            for heading in headings:
                doc = doc.replace(str(heading), "")
            temp_docs.append(doc)
        return temp_docs

    # {|table |} wiki문법 table를 제거
    def _remove_wikitable(self, docs):
        temp_docs = []
        for doc in docs:
            wikicode = mwparserfromhell.parse(doc)
            tags = wikicode.filter_tags(matches=lambda node: node.tag == "table")
            for tag in tags:
                doc = doc.replace(str(tag), "")
            temp_docs.append(doc)
        return temp_docs

    # {| |} wiki문법 table를 제거
    def _remove_wikitable2(self, docs):
        temp_docs = []
        for doc in docs:
            for i in range(100):
                start = doc.find('{|')
                if start > 0 and doc.find('|}', start) > 0:
                    doc = doc[:doc.find('{|')] + doc[doc.find('|}', start) + 2:]
                else:
                    break
            temp_docs.append(doc)
        return temp_docs

    # [[파일: ]], [[분류: ]] wiki문법 link 제거
    def _remove_wikilinks(self, docs):
        temp_docs = []
        for doc in docs:
            wikicode = mwparserfromhell.parse(doc)
            wikilinks = wikicode.filter_wikilinks()
            for wikilink in wikilinks:
                if str(wikilink).find("파일:") > 0:
                    doc = doc.replace(str(wikilink), "")
                if str(wikilink).find("분류:") > 0:
                    doc = doc.replace(str(wikilink), '.' + wikilink[5:-2])
            temp_docs.append(doc)
        return temp_docs

    def _remove_wikilinks2(self, docs):
        temp_docs = []
        for doc in docs:
            wikicode = mwparserfromhell.parse(doc)
            wikilinks = wikicode.filter_wikilinks()
            for wikilink in wikilinks:
                if str(wikilink).find("파일:") > 0:
                    doc = doc.replace(str(wikilink), "")
                if str(wikilink).find("분류:") > 0:
                    doc = doc.replace(str(wikilink), wikilink[5:-2])
            temp_docs.append(doc)
        return temp_docs

    # [ ] wiki문법 externalLink 제거
    def _remove_externalLink(self, docs):
        temp_docs = []
        for doc in docs:
            wikicode = mwparserfromhell.parse(doc)
            externalLinks = wikicode.filter_external_links()
            for externalLink in externalLinks:
                doc = doc.replace(str(externalLink),' '.join(externalLink.split(' ')[1:]))
            temp_docs.append(doc)
        return temp_docs

    # [[ ]] , ''' ''', * wiki 문법 제적
    def _remove_extra(self, docs):
        temp_docs = []
        for doc in docs:
            wikicode = mwparserfromhell.parse(doc)
            doc = wikicode.strip_code()
            temp_docs.append(doc)
        return temp_docs

    # HTML 태그 제거
    def _remove_html(self, docs):
        temp_docs = []
        for doc in docs:
            doc = BeautifulSoup(doc, 'html.parser').text
            temp_docs.append(doc)
        return temp_docs

    # \n 제거
    def _remove_space(self, docs):
        return [doc.replace('\n', '') for doc in docs]

    # .dot을 기준으로 문장을 분리
    def _text2sentence(self, texts):
        temp_texts = []
        for text in texts:
            split_text = text.replace('\r', '').replace('\n', '****').replace('.', '****').split("****")
            split_text = filter(lambda text: text.strip() != "", split_text)
            split_text = map(lambda text: text.strip(), split_text)
            text = '.'.join(split_text)
            temp_texts.append(text)
        return temp_texts

    # [ ] wiki 문법 외부 링크 제거
    def _remove_template_externalLink(self, docs):
        temp_docs = []
        for doc in docs:
            wikicode = mwparserfromhell.parse(doc)
            externalLinks = wikicode.filter_external_links()
            for externalLink in externalLinks:
                if externalLink.find('[') > -1 and externalLink.find(']') > -1:
                    wikicode = mwparserfromhell.parse(externalLink)
                    doc = wikicode.strip_code()
            temp_docs.append(doc)
        return temp_docs

    def _remove_template_wikilinks(self, docs):
        temp_docs = []
        for doc in docs:
            wikicode = mwparserfromhell.parse(doc)
            wikilinks = wikicode.filter_wikilinks()
            for wikilink in wikilinks:
                temp = wikilink.replace('[[', '')
                temp = temp.replace(']]', '')
                if temp.find("|") > -1:
                    temp = temp.split("|")[-1].strip()
                if doc.find(str(wikilink)) > -1:
                    doc = doc.replace(str(wikilink), str(temp))
            temp_docs.append(doc)
        return temp_docs

    # if str(wikilink).find("[[") > -1 and str(wikilink).find("]]") > -1:
    #     doc = doc.replace("[[", "")
    #     doc = doc.replace("]]", "")
    #     if doc.find("|") > -1:
    #         doc = doc.split("|")[-1].strip()

    # () 괄호안에 데이터 제거
    def _remove_parenthesis(self, docs):
        temp_docs = []
        for doc in docs:
            if doc.find('(') > -1 and doc.find(')') > -1:
                doc = re.sub(r'\([^)]*\)', '', doc)
            temp_docs.append(doc)
        return temp_docs

    def _nomalize(self, values):

        temp_values = []
        p = re.compile(r"(\d\d\d\d)\s([\d]?\d)\s([\d]?\d)")
        for val in values:
            days = p.findall(val)
            if len(days) > 0:
                temp_s = ""
                for day in days:
                    temp = []
                    temp.append(day[0] + "년")
                    temp.append(day[1] + "월")
                    temp.append(day[2] + "일")
                    temp_s += " ".join(temp)
                    temp_s += " "
                temp_values.append(temp_s.strip())
            else:
                temp_values.append(val.strip())
        return temp_values

    def _remove_mutiple_spaces(self, docs):
        temp_docs = []
        for doc in docs:
            temp_docs.append(" ".join(doc.split()))
        return temp_docs