class Entity:
    def __init__(self, name):
        self.name = name
        self.properties = []
        self.relations = []

    def add_property(self, prop):
        self.properties.append(prop)

    def add_relation(self, relation):
        self.relations.append(relation)

class Property:
    def __init__(self, name, prop_type):
        self.name = name
        self.type = prop_type
        self.constraints = []

# Relation types
ONE_TO_ONE = 'one-to-one'
ONE_TO_MANY = 'one-to-many'
MANY_TO_ONE = 'many-to-one'
MANY_TO_MANY = 'many-to-many'

class Relation:
    def __init__(self, property_name, property_type, related_entity_name, related_entity_pk, relation_type):
        self.property_name = property_name
        self.property_type = property_type
        self.related_entity_name = related_entity_name
        self.related_entity_pk = related_entity_pk
        self.type = relation_type
