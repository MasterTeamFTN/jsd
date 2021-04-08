from utils import get_current_time, find_pk_property, find_entity
from models import Entity, Property, Relation, ONE_TO_ONE, MANY_TO_MANY, ONE_TO_MANY
from validators import  check_multiple_entity_names, check_multiple_property_name
from mappings import constraints

def copy_properties(entity):
    """
    Method used to extract properties from copy attribute of entity structure
    and place them into entity.properties
    """
    if entity.copy is not None:
        properties_to_copy = entity.copy.properties

        for prop in properties_to_copy:
            if any(prop_from_entity.name == prop.name for prop_from_entity in entity.properties):
                prop.name = prop.name + '_copied'
            entity.properties.append(prop)
def extends_properties(entity, structure, entities):
    if structure.extends is not None:
        main_entity = find_entity(structure.name, entities)
        related_entity = find_entity(structure.extends.name, entities)

        related_entity_pk_property = find_pk_property(structure.extends.properties)
        name = f'{related_entity.name}_{related_entity_pk_property.name}'.lower()

        relation = Relation(name, related_entity_pk_property.type, related_entity.name, related_entity_pk_property.name,
                            ONE_TO_ONE)
        main_entity.add_relation(relation)
