def check_multiple_entity_names(name, entities):
    """
    Check if new entity's 'name' exists in the list of entities
    """
    elements = list(filter(
        lambda e: e.name == name, entities
    ))

    return len(elements) == 1


def check_multiple_property_name(name, properties):
    """
    Check if property 'name' already exists in the list of given properties
    """
    elements = list(filter(
        lambda p: p.name == name, properties
    ))

    return len(elements) == 1
def check_property_type(name, types):
    """
    Check if property 'name' already exists in the list of given properties
    """
    elements = list(filter(
        lambda p: p.name == name, types
    ))

    return len(elements) == 1


def check_duplicate_constraints(entities):
    """
    Checks all properties to see whether there are duplicate
    constraints on specific property
    Returns status, and entity and prop if error exists
    """
    for entity in entities:

        if hasattr(entity, 'properties'):
            for prop in entity.properties:
                if len(prop.constraints) != len(set(prop.constraints)):
                    return True, entity, prop

    return False, None, prop


def check_multiple_pk(entities):
    """
    Checks if there are multiple primary keys in one entity
    Returns status and entity if error exists
    """
    for entity in entities:
        # Collect all properties from 1 entity
        constraints = []

        if hasattr(entity, 'properties'):
            for prop in entity.properties:
                for constraint in prop.constraints:
                    constraints.append(constraint)

            # Duplicated exist
            if constraints.count('PRIMARY KEY') > 1:
                return True, entity

    return False, None

def check_pk_exists(entities):
    """
    Checks if there are multiple primary keys in one entity
    Returns status and entity if error exists
    """
    for entity in entities:
        # Collect all properties from 1 entity
        constraints = []
        if hasattr(entity, 'properties'):
            for prop in entity.properties:
                for constraint in prop.constraints:
                    constraints.append(constraint)

            # Duplicated exist
            if constraints.count('PRIMARY KEY') == 0:
                return True, entity

    return False, None
