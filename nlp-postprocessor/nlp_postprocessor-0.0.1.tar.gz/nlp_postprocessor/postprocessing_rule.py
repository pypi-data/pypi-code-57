class PostprocessingRule:

    def __init__(self, patterns, action, name=None, description=None, action_args=None):
        """A PostprocessingRule checks conditions of a spaCy Span entity
        and executes some action if all patterns are met.

        patterns (list): A list of PostprocessingPatterns,
            each of which check a condition of an entity.
        action (function): A function to call with the entity as an argument.
            This function should take ay least the following two arguments:
                ent: the spacy span
                i: the index of ent in doc.ents
            Additional positional arguments can be provided in action_args.
        name (str): Optional name of rule.
        description (str): Optional description of the rule.
        action_args (tuple or None): Optional tuple of positional arguments
            to pass to action() if all patterns pass. Default is None,
            in which case the rule will call action(ent, i).

        """
        self.patterns = patterns
        self.action = action
        self.name = name
        self.description = description
        self.action_args = action_args

    def __call__(self, ent, i, debug=False):
        """Iterate through all of the patterns in self.rules.
        If any pattern does not pass (ie., return True), then returns False.
        If they all pass, execute self.action and return True.
        """
        for pattern in self.patterns:
            # If this is a tuple, at least one has to pass
            if isinstance(pattern, tuple):
                passed = False
                for subpattern in pattern:
                    rslt = subpattern(ent)
                    if rslt is True:
                        passed = True
                        break
                if passed is False:
                    return False
            # Otherwise just check a single value
            else:
                rslt = pattern(ent)
                if rslt is False:
                    return False

        # Every pattern passed - do the action
        if debug:
            print("Passed:", self, "on ent:", ent, ent.sent)
        if self.action_args is None:
            self.action(ent, i)
        else:
            self.action(ent, i, *self.action_args)
        return True

    def __repr__(self):
        return f"PostprocessingRule: {self.name} - {self.description}"