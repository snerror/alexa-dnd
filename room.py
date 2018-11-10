import json


class Room:
    def __init__(self):
        self.open = 0
        self.description = 'some room'

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
