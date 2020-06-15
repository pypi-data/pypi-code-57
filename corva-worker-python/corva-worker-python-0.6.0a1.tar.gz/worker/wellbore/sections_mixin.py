class SectionsMixin(object):
    def __init__(self, *args, **kwargs):
        self.sections = []

    def __len__(self):
        return len(self.sections)

    def __getitem__(self, index):
        return self.sections[index]

    def __delitem__(self, index):
        del self.sections[index]

    def __bool__(self):
        return len(self) != 0

    def __repr__(self):
        return "\n".join(str(sec) for sec in self.sections)
