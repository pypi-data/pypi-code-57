from tokenizer_tools.tagset.offset.span import Span


class EntityPlaceholder(Span):
    def render(self, value):
        # inplace render
        self.value = value

    def __str__(self):
        return "{}".format(self.entity)
