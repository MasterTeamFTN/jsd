import sys
from os import mkdir
from os.path import exists, dirname, join
import jinja2
from textx import metamodel_from_file
from models import Entity, Property
from utils import get_current_time

this_folder = dirname(__file__)

constraints = {
    'pk': 'PRIMARY KEY',
    'notnull': 'NOT NULL',
    'unique': 'UNIQUE'
}

def get_mm():
    """
    Builds and returns a meta-model for our language.
    """
    return metamodel_from_file(join(this_folder, 'grammars', 'grammar.tx'))

def init_template_engine(path):
    # Initialize the template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Load template
    template_path = join('templates', 'sql_create.template')
    return jinja_env.get_template(template_path)


def main(model_filename, debug=False):
    # Instantiate meta-model
    mm = get_mm()

    # Create the output folder
    srcgen_folder = join(this_folder, 'srcgen')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    template = init_template_engine(this_folder)

    # Build a model from input file
    model = mm.model_from_file(model_filename)


    database_name = model.config.db_name

    entities = []

    for structure in model.structures:
        if structure.__class__.__name__ == 'Entity':
            entity = Entity(structure.name)
            entities.append(entity)

            for prop in structure.properties:
                p = Property(prop.name, prop.type)
                entity.properties.append(p)

                if prop.constraints != None:
                    for constraint in prop.constraints.constraints:
                        p.constraints.append(constraints[constraint])

        else: # 'Field'
            # @TODO: Finish this
            pass

    
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
            template.render(
                entities=entities, 
                database_name=database_name,
                time=get_current_time()
            )
        )


def check_duplicate_constraints(entities):
    """
    Checks all properties to see whether there are duplicate
    constraints on specific property
    Returns status, and entity and prop if error exists
    """
    for entity in entities:
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

        for prop in entity.properties:
            for constraint in prop.constraints:
                constraints.append(constraint)

        # Duplicated exist
        if len(constraints) != len(set(constraints)):
            return True, entity

    return False, None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Enter file name as first parameter')
        exit(1)

    filename = sys.argv[1]
    print(f'File to interpret: {filename}')

    main(filename)
