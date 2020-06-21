from typing import List


class TokenStream:
    head: int
    tokens: List

    def __init__(self, tokens: List):
        self.head = 0
        self.tokens = tokens

    def consume(self):
        result = self.tokens[self.head]
        self.head += 1
        return result

    def left_overs(self):
        return self.tokens[self.head:]

    def is_drained(self):
        return self.head == len(self.tokens)

    def set_to(self, head: int):
        self.head = head

    def peek(self):
        return self.tokens[self.head]

    @classmethod
    def from_iterator(cls, it):
        tokens_list = []
        for token in it:
            tokens_list.append(token)

        return TokenStream(tokens_list)
