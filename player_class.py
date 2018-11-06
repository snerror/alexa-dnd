import json


class PlayerClass:
    def __init__(self, name, strength, intellect):
        self.name = name
        self.attributes = PlayerAttributes(strength, intellect)

    def toJSON(self):
        return json.dumps(self)


class PlayerAttributes:
    def __init__(self, strength, intellect):
        self.strength = strength
        self.intellect = intellect
