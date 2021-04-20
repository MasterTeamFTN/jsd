import os
from os import mkdir
from os.path import exists, dirname, join

import click
from textx import metamodel_from_file, generator
from textx.exceptions import TextXSemanticError
from textx.exceptions import TextXSyntaxError

from .mappings import constraints
from .mappings import get_type
from .models import Entity, Property, SimpleType
from .properties_manager import copy_properties, extends_properties, fix_entity_order
from .relations_manager import manage_relations
from .template_engine import init_template_engine
from .utils import get_current_time, write_to_file
from .validators import check_duplicate_constraints, check_multiple_entity_names, check_multiple_pk, check_pk_exists, \
    check_multiple_property_name

this_folder = dirname(__file__)
databases = ['mysql', 'postgresql']
from textx import LanguageDesc


def get_mm():
    """
    Builds and returns a meta-model for our language.
    """
    type_builtins = {
        'integer': SimpleType(None, 'integer'),
        'string': SimpleType(None, 'string'),
        'float': SimpleType(None, 'float')
    }
    return metamodel_from_file(join(this_folder, 'grammar.tx'), classes=[SimpleType],
                               builtins=type_builtins)




def main(model_filename):
    # Instantiate meta-model
    mm = get_mm()

    # Create the output folder
    srcgen_folder = join(this_folder, 'srcgen')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    # Build a model from input file
    try:
        model = mm.model_from_file(model_filename)
    except (TextXSyntaxError, TextXSemanticError) as error:
        print('Compilation failed...')
        print(error)
        return None, None

    database_name = model.config.db_name
    if not database_name in databases:
        print(f'Error - Unknown database \'{database_name}\'. Supported databases: mysql and postgresql')
        return None, None
    # TODO: check here if we support this database
    # You can check if model.config.db_name exists
    # as a key of types dictionary, or something like that

    entities = []

    # First pass - create entities and basic properties
    for structure in model.structures:
        if structure.__class__.__name__ != 'Entity':
            continue

        if check_multiple_entity_names(structure.name, entities):
            print(f'Error - Entity with name \'{structure.name}\' already exists')
            return None, None

        # Handle fields and copy
        if hasattr(structure, 'copy'):
            copy_properties(structure)

        entity = Entity(structure.name)
        entities.append(entity)

        for prop in structure.properties:
            # TODO: add here prop.manyToOne if needed
            if prop.oneToMany or prop.manyToMany or prop.oneToOne:
                continue

            if check_multiple_property_name(prop.name, entity.properties):
                print(f'Error - Property \'{prop.name}\' of entity \'{entity.name}\' already exists.')
                return None, None

            p = Property(prop.name, get_type(prop.type, database_name))
            entity.add_property(p)
            if prop.constraints is not None:
                for constraint in prop.constraints.constraints:
                    p.constraints.append(constraints[constraint])

    status, entity = check_pk_exists(entities)
    if status:
        print(f'Error - Entity \'{entity.name}\' has no primary key')
        return None, None

    # Second pass - create relations
    for structure in model.structures:
        if structure.__class__.__name__ == 'Entity':
            structure.properties = manage_relations(structure, entities, database_name)

            if hasattr(structure, 'extends'):
                extends_properties(entity, structure, entities, database_name)

    # Validate constraints
    status, entity, prop = check_duplicate_constraints(entities)
    if status:
        print(f'Error - Property \'{prop.name}\' of entity \'{entity.name}\' has duplicate constraints')
        return None, None

    status, entity = check_multiple_pk(entities)
    if status:
        print(f'Error - Entity \'{entity.name}\' has more than one primary key')
        return None, None

    # Fix entity order to generate valid sql script
    entities = fix_entity_order(entities)

    return entities, database_name

@generator('jsd_language', 'sql')
def sql_generator(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generates sql script from sg file."
    input_file = model._tx_filename

    base_dir = output_path if output_path else os.path.dirname(input_file)
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    output_file = os.path.abspath(
        os.path.join(base_dir, "{}.{}".format(base_name, 'sql'))
    )

    if overwrite or not os.path.exists(output_file):
        click.echo('-> {}'.format(output_file))
        entities, database_name = main(input_file)

        if entities == None:
            return

        sql_template = init_template_engine(this_folder, 'sql_create.template')

        data = sql_template.render(
            entities=entities,
            database_name=database_name,
            time=get_current_time()
        )

        write_to_file(output_file, data)
        print('Successful compilation')
        print(f'SQL Script generated at: {output_file}')
    else:
        click.echo('-- Skipping: {}'.format(output_file))


@generator('jsd_language', 'dot')
def dot_generator(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generates dot file from sg file."
    input_file = model._tx_filename

    base_dir = output_path if output_path else os.path.dirname(input_file)
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    output_file = os.path.abspath(
        os.path.join(base_dir, "{}.{}".format(base_name, 'dot'))
    )

    if overwrite or not os.path.exists(output_file):
        click.echo('-> {}'.format(output_file))
        entities, database_name = main(input_file)

        if entities == None:
            return

        dot_template = init_template_engine(this_folder, 'dot_create.template')

        data = dot_template.render(
            entities=entities,
            database_name=database_name,
            time=get_current_time()
        )

        write_to_file(output_file, data)
        print('Successful compilation')
        print(f'ER diagram generated at: {output_file}')

        click.echo('   To convert to png run "dot -Tpng -O {}"'
                   .format(os.path.basename(output_file)))
    else:
        click.echo('-- Skipping: {}'.format(output_file))

jsd_lang = LanguageDesc('jsd_language',
                        pattern='*.sg',
                        description='Entity-relationship language',
                        metamodel=get_mm)

