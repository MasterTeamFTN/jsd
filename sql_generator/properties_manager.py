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
