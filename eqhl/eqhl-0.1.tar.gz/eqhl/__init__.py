colors = ['blue', 'yellow', 'cyan', 'orange', 'green', 'purple']
choice = 0


def pick_color():
    global choice
    color = colors[choice]

    choice = (choice + 1) % 6
    return color


class Term:
    """ A normal term """
    def __init__(self, tex):
        self.tex = tex
        self.html = r'<li>\({}\)</li>'.format(self.tex)


class HLTerm(Term):
    """ A term to be highlighted """
    def __init__(self, tex, label):
        self.tex = tex
        self.label = label
        self.html = r'<li class="{}" title="{}">\({}\)</li>'.format(pick_color(), self.label, self.tex)


class Equation:
    """ Equations are ordered collections of terms and HLTerms """
    def __init__(self, terms):
        self.terms = terms

    @property
    def tex(self):
        # Join terms into single string of tex
        return '$$' + ''.join([term.tex for term in self.terms]) + '$$'

    @property
    def html(self):
        return '<ul class="equation">\n\t{}\n</ul>'.format('\n\t'.join([term.html for term in self.terms]))

    def append(self, term):
        self.terms.append(term)

    # Printing an equation displays its tex representation
    def __str__(self):
        return self.tex
