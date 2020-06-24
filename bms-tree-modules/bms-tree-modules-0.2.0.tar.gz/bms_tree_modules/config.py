from typing import Dict, List, Union


class EffectConfig(object):
    def __init__(self, period_input):
        self.name: str
        self.values: Dict[str, Union[str, float]] = {}
        self.__check_input(period_input)

    def __check_input(self, period_input):
        if isinstance(period_input, dict):
            self.from_dict(period_input)
        else:
            raise TypeError(
                "Expected: period_input <class 'dict'>, Received: {0}".format(
                    type(period_input)
                )
            )

    def from_dict(self, period_input: dict):
        self.name = period_input["name"]

        for param in period_input["values"]:
            key_ = param["key"]

            if key_ in ["MIN", "MAX", "WEIGHT"]:
                self.values[key_] = float(param["value"])
            else:
                self.values[key_] = param["value"]

    def value(self, key: str) -> Union[str, float]:
        return self.values[key]


class NodeConfig(object):
    def __init__(self, period_input):
        self.effects: List[EffectConfig] = []
        self.name: str
        self.__check_input(period_input)

    def __check_input(self, period_input):
        if isinstance(period_input, dict):
            self.from_dict(period_input)
        else:
            raise TypeError(
                "Expected: period_input <class 'dict'>, Received: {0}".format(
                    type(period_input)
                )
            )

    def from_dict(self, period_input: dict):
        """create a EffectConfig for each effect in the input
        An EffectConfig is composed of:
        - name: str
        - values: dict - key-value pairs containing the configuration values
        """
        self.name = period_input["name"]
        self.effects = [EffectConfig(effect) for effect in period_input["effects"]]

    def effect(self, name: str) -> EffectConfig:
        if not isinstance(name, str):
            raise TypeError(
                "Expected: name <class 'str'>, Received: {0}".format(type(name))
            )

        # retrieve the effect by its name
        effect = list(filter(lambda effect: effect.name == name, self.effects))

        # check if an entry was found, else throw an exception
        if len(effect) == 1:
            return effect[0]
        else:
            raise ValueError("No effect found for: name '{0}'".format(name))

    def value(self, effect: str, value: str) -> Union[str, float]:
        return self.effect(effect).value(value)


class ModuleConfig(object):
    def __init__(self, period_input):
        self.configurations: List[NodeConfig] = []

        # process period_input and convert into objects
        self.__check_input(period_input)

    def __check_input(self, period_input):
        if isinstance(period_input, dict):
            self.from_dict(period_input)
        else:
            raise TypeError(
                "Expected: period_input <class 'dict'>, Received: {0}".format(
                    type(period_input)
                )
            )

    def node_names(self) -> List[str]:
        return list(map(lambda node: node.name, self.configurations))

    def node(self, name: str) -> NodeConfig:
        if not isinstance(name, str):
            raise TypeError(
                "Expected: name <class 'str'>, Received: {0}".format(type(name))
            )

        # retrieve the node by its name
        node = list(filter(lambda node: node.name == name, self.configurations))

        # check if an entry was found, else throw an exception
        if len(node) == 1:
            return node[0]
        else:
            raise ValueError("No node found for: name '{0}'".format(name))

    def effect(self, name: str, effect: str) -> EffectConfig:
        return self.node(name).effect(effect)

    def value(self, name: str, effect: str, value: str) -> Union[str, float]:
        return self.effect(name, effect).value(value)

    def from_dict(self, period_input: dict):
        """create a NodeConfig object for each (Leaf-)Node in the input json.
        A NodeConfig is composed of:
        - name: str
        - effects: List[Effects] - effects which are used during the state computation
        """
        self.configurations = [NodeConfig(node) for node in period_input["config"]]
