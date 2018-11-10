import json

WARRIOR = "warrior"
WIZARD = "wizard"


class PlayerClass:
    def __init__(self, chosen_class):
        if chosen_class == WARRIOR:
            self.class_name = WARRIOR
            self.hp = 10
            self.ac = 17
            self.surge = 5
        elif chosen_class == WIZARD:
            self.class_name = WIZARD
            self.hp = 6
            self.ac = 14
            self.surge = 3
        else:
            self.class_name = 'test'
            self.hp = 1
            self.ac = 1
            self.surge = 1

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
