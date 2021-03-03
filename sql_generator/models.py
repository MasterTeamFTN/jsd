class Entity:
    def __init__(self, name):
        self.name = name
        self.properties = []

class Property:
    def __init__(self, name, prop_type):
        self.name = name
        self.type = prop_type
        self.constraints = []
