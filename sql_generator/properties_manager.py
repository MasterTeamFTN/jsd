from utils import get_current_time, find_pk_property, find_entity
from models import Entity, Property, Relation, ONE_TO_ONE, MANY_TO_MANY
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
        properties_to_copy = structure.extends

        if not check_multiple_entity_names(properties_to_copy.name, entities):
            newEntity = Entity(properties_to_copy.name)
            entities.append(newEntity)

            for prop in structure.extends.properties:
                if prop.oneToMany or prop.manyToMany or prop.oneToOne:
                    continue

                if check_multiple_property_name(prop.name, newEntity.properties):
                    print(f'Error - Property \'{prop.name}\' of entity \'{newEntity.name}\' already exists.')
                    return

                p = Property(prop.name, prop.type)
                newEntity.add_property(p)

                if prop.constraints is not None:
                    for constraint in prop.constraints.constraints:
                        p.constraints.append(constraints[constraint])

        related_entity_pk_property = find_pk_property(structure.extends.properties)
        name = f'{structure.extends.name}_{related_entity_pk_property.name}'.lower()

        relation = Relation(name, related_entity_pk_property.type, structure.extends.name, related_entity_pk_property.name,
                            ONE_TO_ONE)
        entity.add_relation(relation)
