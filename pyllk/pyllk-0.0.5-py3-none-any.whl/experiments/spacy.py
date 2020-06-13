import json

from pyllk.token import TerminalToken


class SpacyToken(TerminalToken):
    def __init__(self):
        super().__init__(representation={})

    def text(self, text):
        self.representation['TEXT'] = text
        return self

    def lemma(self, text):
        self.representation['LEMMA'] = text
        return self

    def dependency(self, text):
        self.representation['DEP'] = text
        return self

    def part_of_speech(self, text):
        self.representation['POS'] = text
        return self

    def tag(self, text):
        self.representation['TAG'] = text
        return self

    def entity(self, text):
        self.representation['ENTITY'] = text
        return self

    def regex(self, text):
        self.representation['REGEX'] = text
        return self

    def matches(self, obj):
        match = True

        if 'TEXT' in self.representation:
            match &= (self.representation['TEXT'] == obj.text)

        if 'LEMMA' in self.representation:
            match &= (self.representation['LEMMA'] == obj.lemma_)

        if 'DEP' in self.representation:
            match &= (self.representation['DEP'] == obj.dep_)

        if 'POS' in self.representation:
            match &= (self.representation['POS'] == obj.pos_)

        if 'TAG' in self.representation:
            match &= (self.representation['TAG'] == obj.tag_)

        if 'ENTITY' in self.representation:
            match &= (self.representation['ENTITY'] == obj.ent_type_)

        return match

    def __str__(self):
        return json.dumps(self.representation)
