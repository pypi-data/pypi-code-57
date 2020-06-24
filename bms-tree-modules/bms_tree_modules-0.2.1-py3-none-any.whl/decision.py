from typing import List


class Decision(object):
    def __init__(
        self,
        key: str,
        value: float,
        title: str = "",
        description: str = "",
        helper: bool = False,
    ):
        self.key = key
        self.value = value
        self.title = title
        self.description = description
        self.helper = helper

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value": self.value,
            "title": self.title,
            "description": self.description,
        }


class Decisions(object):
    CONST_KEY = "key"
    CONST_VALUE = "value"
    CONST_TITLE = "title"
    CONST_DESCRIPTION = "description"

    def __init__(self, decisions_input: dict):
        self.decisions = self.__from_dict(decisions_input)

    def __from_dict(self, decisions_input: dict) -> List[Decision]:
        if isinstance(decisions_input, list):
            decisions = []
            for decision_input in decisions_input:
                if isinstance(decision_input, dict):
                    if self.CONST_KEY not in decision_input.keys():
                        raise AttributeError(
                            "decision_input <class 'dict'> has not attribute '{0}'".format(
                                self.CONST_KEY
                            )
                        )

                    if self.CONST_VALUE not in decision_input.keys():
                        raise AttributeError(
                            "decision_input <class 'dict'> has not attribute '{0}'".format(
                                self.CONST_VALUE
                            )
                        )

                    decision = Decision(
                        decision_input[self.CONST_KEY],
                        decision_input[self.CONST_VALUE],
                        decision_input[self.CONST_TITLE],
                        decision_input[self.CONST_DESCRIPTION],
                    )
                    decisions.append(decision)
                else:
                    raise TypeError(
                        "Expected: decision_input <class 'dict'>, Received: {0}".format(
                            type(decision_input)
                        )
                    )
            return decisions
        else:
            raise TypeError(
                "Expected: decisions_input <class 'list'>, Received: {0}".format(
                    type(decisions_input)
                )
            )

    def to_dict(self) -> List[dict]:
        base_decisions = []
        for dec in self.decisions:
            # only return the base decisions created during the initial model creation
            # don't return any helper decisions created as a part of the model evaluation
            if not dec.helper:
                decision_as_dict = dec.to_dict()
                base_decisions.append(decision_as_dict)
        return base_decisions

    def decision(self, key: str) -> Decision:
        decisions = list(filter(lambda decision: decision.key == key, self.decisions))
        if len(decisions) > 0:
            return decisions[0]
        else:
            raise AttributeError("No decision with key '{0}' exists!".format(key))
