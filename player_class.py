import json

WARRIOR = "warrior"
WIZARD = "wizard"


class PlayerClass:
    def __init__(self, chosen_class):
        if chosen_class == WARRIOR:
            self.name = WARRIOR
            self.hp = 10
            self.ac = 17
            self.surge = 5
        elif chosen_class == WIZARD:
            self.name = WIZARD
            self.hp = 6
            self.ac = 14
            self.surge = 3

    def toJSON(self):
        return json.dumps(self)
