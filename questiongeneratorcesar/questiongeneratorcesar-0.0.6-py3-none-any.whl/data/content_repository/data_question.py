class DataQuestion():
    def __init__(self, content, interest, target_lemma, target_word, pos):
        self.content = content
        self.interest = interest
        self.target_lemma = target_lemma
        self.target_word = target_word
        self.pos = pos

    def __repr__(self):
        return "DataQuestion({},'{}','{}','{}')".format(self.content.id, 
                                                self.target_lemma, 
                                                self.target_word, 
                                                self.pos)
