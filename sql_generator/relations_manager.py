from models import Entity, Property, Relation, ONE_TO_MANY, MANY_TO_MANY, MANY_TO_ONE
from utils import get_current_time, find_pk_property, find_entity


def manage_relations(structure, entities):
    '''
    Method used to manage all the manyTomany, oneToMany Todo: ManyToOne
    properties of a structure by removing them and creating inter table if needed
    '''
    non_relation_properties = []

    for property_from_structure in structure.properties:
        if property_from_structure.manyToMany is not None:
            '''
            Handling many to many property
            '''
            ftProp = find_pk_property(structure.properties)
            stProp = find_pk_property(property_from_structure.manyToMany.properties)

            ftEntityName = structure.name
            stEntityName = property_from_structure.manyToMany.name

            entity = Entity(structure.name + "_" + property_from_structure.manyToMany.name)
            # idProperty = Property('id', 'number')
            # idProperty.constraints.append('PRIMARY KEY')
            # entity.properties.append(idProperty)

            firstRelation = Relation(f'{ftEntityName}_{ftProp.name}'.lower(), ftProp.type, ftEntityName, ftProp.name,
                                     MANY_TO_MANY)
            entity.add_relation(firstRelation)

            secondRelation = Relation(f'{stEntityName}_{stProp.name}'.lower(), stProp.type, stEntityName, stProp.name,
                                      MANY_TO_MANY)
            entity.add_relation(secondRelation)

            entities.append(entity)

        elif property_from_structure.oneToMany is not None:
            main_entity = find_entity(structure.name, entities)
            related_entity = find_entity(property_from_structure.oneToMany.name, entities)

            main_entity_pk_property = find_pk_property(structure.properties)
            name = f'{main_entity.name}_{main_entity_pk_property.name}_{property_from_structure.name}'.lower()

            relation = Relation(name, main_entity_pk_property.type, main_entity.name, main_entity_pk_property.name,
                                ONE_TO_MANY)
            related_entity.add_relation(relation)

        elif property_from_structure.manyToOne is not None:
            main_entity = find_entity(structure.name, entities)
            related_entity = find_entity(property_from_structure.manyToOne.name, entities)
            related_entity_pk_property = find_pk_property(property_from_structure.manyToOne.properties)

            name = f'{property_from_structure.name}_{related_entity_pk_property.name}'.lower()

            relation = Relation(
                name, 
                related_entity_pk_property.type, 
                related_entity.name, 
                related_entity_pk_property.name,
                MANY_TO_ONE
            )

            main_entity.add_relation(relation)

        elif property_from_structure.oneToOne is not None:
            # Todo: implement many to one relation
            pass

        elif property_from_structure not in non_relation_properties:
            non_relation_properties.append(property_from_structure)

    return non_relation_properties
