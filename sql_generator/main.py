from os import mkdir
from os.path import exists, dirname, join

from textx import metamodel_from_file
from models import Entity, Property, Relation, ONE_TO_MANY, MANY_TO_MANY
from utils import get_current_time, find_pk_property, find_entity
from mappings import constraints
from validators import check_duplicate_constraints, check_multiple_entity_names, check_multiple_pk, check_multiple_property_name
from command_line import CommandLine

from relations_manager import manage_relations
from template_engine import init_template_engine

from properties_manager import copy_properties

this_folder = dirname(__file__)

def get_mm():
    """
    Builds and returns a meta-model for our language.
    """
    return metamodel_from_file(join(this_folder, 'grammars', 'grammar.tx'))


def main(model_filename, sql_output_file, dot_output_file, dot_only, sql_only, debug=False):
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

        structure.properties = manage_relations(structure, entities)

        for prop in structure.properties:
            if check_multiple_property_name(prop.name, entity.properties):
                print(f'Error - Property \'{prop.name}\' of entity \'{entity.name}\' already exists.')
                return

            p = Property(prop.name, prop.type)
            entity.add_property(p)

            if prop.constraints is not None:
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
    if not dot_only:
        with open(sql_output_file, 'w') as f:
            f.write(
                sql_template.render(
                    entities=entities,
                    database_name=database_name,
                    time=get_current_time()
                )
            )

    # Generate dot
    if not sql_only:
        dot_template = init_template_engine(this_folder, 'dot_create.template')
        with open(dot_output_file, 'w') as f:
            f.write(
                dot_template.render(
                    entities=entities,
                    database_name=database_name,
                    time=get_current_time()
                )
            )



if __name__ == '__main__':
    app = CommandLine()
    main(app.args.sourceFile, app.args.sqlFile, app.args.dotFile, app.args.dotOnly, app.args.sqlOnly)
