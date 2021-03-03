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


def init_template_engine(path):
    """
    Initialize jinja template engine
    """
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
    # TODO: check here if we support this database
    # You can check if model.config.db_name exists
    # as a key of types dictionary, or something like that

    entities = []

    for structure in model.structures:
        if structure.__class__.__name__ == 'Entity':
            if check_multiple_entity_names(structure.name, entities):
                print(f'Error - Entity with name \'{structure.name}\' already exists')
                return

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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Enter file name as first parameter')
        exit(1)

    filename = sys.argv[1]
    print(f'File to interpret: {filename}')

    main(filename)
