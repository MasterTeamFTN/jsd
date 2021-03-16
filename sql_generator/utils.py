from datetime import datetime
import argparse

def get_current_time():
    return datetime.now()

def find_pk_property(properties):
    """
    Method used to find property labeled with pk. That kind of properties represent
    fields that are going to be primary keys of the tables they are in.
    """
    for prop in properties:
        if 'pk' in prop.constraints.constraints:
            return prop

def find_entity(name, entities):
    """
    Method used to find entity from list of entities by entity name
    """
    for entity in entities:
        if entity.name == name:
            return entity
    return None


def str2bool(v):
    """
    Method used to convert string with value known to boolean classification into boolean

    True    == yes, true, t, y, 1 (case insensitive)
    False   == no, false, f, n, 0 (case insensitive)
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')