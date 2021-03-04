import sys
from os import mkdir
from os.path import exists, dirname, join
import jinja2
from textx import metamodel_from_file
from models import Entity, Property
from utils import get_current_time
from mappings import constraints
from validators import check_duplicate_constraints, check_multiple_entity_names, check_multiple_pk, check_multiple_property_name

this_folder = dirname(__file__)

def get_mm():
    """
    Builds and returns a meta-model for our language.
    """
    return metamodel_from_file(join(this_folder, 'grammars', 'grammar.tx'))


def init_template_engine(path, template_name):
    """
    Initialize jinja template engine
    """
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Load template
    template_path = join('templates', template_name)
    return jinja_env.get_template(template_path)


def copy_properties(entity):
    """
    Method used to extract properties from copy attribute of entity structure
    and place them into entity.properties
    """
    if entity.copy is not None:
        properties_to_copy = entity.copy.properties

        for prop in properties_to_copy:
            if any(property.name == prop.name for property in entity.properties):
                prop.name = prop.name + '_copied'
            entity.properties.append(prop)


def main(model_filename, debug=False):
    # Instantiate meta-model
    mm = get_mm()

    # Create the output folder
    srcgen_folder = join(this_folder, 'srcgen')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    sql_template = init_template_engine(this_folder, 'sql_create.template')

    # Build a model from input file
    model = mm.model_from_file(model_filename)

    database_name = model.config.db_name
    # TODO: check here if we support this database
    # You can check if model.config.db_name exists
    # as a key of types dictionary, or something like that

    entities = []

    for structure in model.structures:
        if structure.__class__.__name__ != 'Entity':
            continue

        if check_multiple_entity_names(structure.name, entities):
            print(f'Error - Entity with name \'{structure.name}\' already exists')
            return

        # Handle fields and copy 
        if hasattr(structure, 'copy'):
            copy_properties(structure)

        entity = Entity(structure.name)
        entities.append(entity)

        for prop in structure.properties:
            if check_multiple_property_name(prop.name, entity.properties):
                print(f'Error - Property \'{prop.name}\' of entity \'{entity.name}\' already exists.')
                return

            p = Property(prop.name, prop.type)
            entity.add_property(p)

            if prop.constraints != None:
                for constraint in prop.constraints.constraints:
                    p.constraints.append(constraints[constraint])
    
    # Validate constraints
    status, entity, prop = check_duplicate_constraints(entities)
    if status:
        print(f'Error - Property \'{prop.name}\' of entity \'{entity.name}\' has duplicate constraints')
        return

    status, entity = check_multiple_pk(entities)
    if status:
        print(f'Error - Entity \'{entity.name}\' has more than one primary key')
        return

    # Generate SQL code
    with open(join(srcgen_folder, "create_db_schema.sql"), 'w') as f:
        f.write(
            sql_template.render(
                entities=entities, 
                database_name=database_name,
                time=get_current_time()
            )
        )

    # Generate dot
    dot_template = init_template_engine(this_folder, 'dot_create.template')
    
    with open(join(srcgen_folder, 'er_diagram.dot'), 'w') as f:
        f.write(
            dot_template.render(
                entities=entities,
                database_name=database_name,
                time=get_current_time()
            )
        )



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Enter file name as first parameter')
        exit(1)

    filename = sys.argv[1]
    print(f'File to interpret: {filename}')

    main(filename)
