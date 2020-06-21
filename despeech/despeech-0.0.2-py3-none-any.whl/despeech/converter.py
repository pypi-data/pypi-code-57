from nltk.tokenize import word_tokenize
from uralicNLP import uralicApi

from uralicNLP.cg3 import Cg3


class DeSpeechConverter:
    PREFIXES = ['ab', 'bei', 'auf', 'ein', 'vor', 'aus', 'mit', 'an', 'nach']
    CONJUNCTIVES = ['wohin', 'woher', 'wie lange', 'wie oft', 'warum', 'wieso', 'wie viel', 'dass', 'ob']
    LANGUAGE = 'deu'

    def __init__(self):
        self._model = Cg3(self.LANGUAGE)

    def _disambiguate(self, model, tokens):
        results = []
        disambiguations = model.disambiguate(tokens)
        for disambiguation in disambiguations:
            possible_words = disambiguation[1]
            results.append(possible_words)
        return results

    def _get_verb(self, results):
        for result in results:
            for single_parsing in result:
                if 'V' in single_parsing.morphology:
                    return result

    def _separate_sentence_with_direct_speech(self, text):
        part1 = text[:text.find('"')]
        direct_part = text[text.find('"'):]
        return part1, direct_part

    def _separate_sentence_with_indirect_speech(self, text):
        part1 = text[:text.find(',')]
        direct_part = text[text.find(','):]
        return part1, direct_part

    def _find_subject(self, disamb_part_of_sent):
        for i, word_parsing_results in enumerate(disamb_part_of_sent):
            for single_parsing_result in word_parsing_results:
                if 'Nom' in single_parsing_result.morphology:
                    subject = single_parsing_result.lemma
                    if 'Det' in single_parsing_result.morphology:
                        subject = str(disamb_part_of_sent[i][0].lemma) + ' ' + str(disamb_part_of_sent[i + 1][0].lemma)
                    return subject

    def generate_new_subject(self, disamb_part1):
        for i, word_parsing_results in enumerate(disamb_part1):
            for single_parsing_result in word_parsing_results:
                if 'Nom' in single_parsing_result.morphology:
                    sub_morphology = single_parsing_result.morphology
                    if 'Pron' in sub_morphology:
                        return single_parsing_result.lemma, single_parsing_result.morphology[2]
                    if "Msc" in sub_morphology:
                        if "Sg" in sub_morphology:
                            return 'er', 'Sg3'
                        else:
                            return 'sie', 'Pl3'
                    else:
                        if 'Sg' in sub_morphology:
                            return 'sie', 'Sg3'
                        else:
                            return 'sie', 'Pl3'

    def _change_verb_in_direct_part(self, disamb_direct_part, new_subject_form, language):
        for word in disamb_direct_part:
            for i in word:
                if 'V' in i.morphology:
                    verb_lemma = i.lemma
                    verb_morphology = i.morphology[:5]
                    new_morphology = []
                    for elem in verb_morphology:
                        if elem.startswith("<"):
                            continue
                        if elem.startswith('Sg'):
                            elem = new_subject_form

                        new_morphology.append(elem)
                    new_morphology = str(new_morphology)
                    new_morphology = new_morphology.replace(', ', '+')
                    new_morphology = new_morphology.replace('\'', '')
                    new_morphology = new_morphology.strip('[]')
                    form_for_generating = str(verb_lemma) + '+' + new_morphology
                    verb_new_form = uralicApi.generate(form_for_generating, language)[0][0]
                    return verb_new_form

    def convert(self, text):
        text = text.lower()
        if '"' in text:
            parts_of_sents = self._separate_sentence_with_direct_speech(text)
            disamb_part1 = self._disambiguate(self._model, word_tokenize(str(parts_of_sents[0])))
            disamb_part2 = self._disambiguate(self._model, word_tokenize(str(parts_of_sents[1])))
            subject2 = self._find_subject(disamb_part2)
            verb_initial_form = self._get_verb(disamb_part2)[0].form
            new_subject, new_subject_form = self.generate_new_subject(disamb_part1)

            if subject2 == 'du' or subject2 == 'Sie':
                new_subject = "ich"
                new_subject_form = 'Sg1'
            if subject2 == 'ihr':
                new_subject = 'sie'
                new_subject_form = 'Pl3'
            verb_new_form = self._change_verb_in_direct_part(disamb_part2, new_subject_form, self.LANGUAGE)

            first_part = parts_of_sents[0].replace(':', ',')
            second_part = parts_of_sents[1].replace('"', '')
            second_part = second_part.replace(subject2, new_subject)
            second_part = second_part.replace(verb_initial_form, verb_new_form)
            result = first_part + " " + second_part
            return result
