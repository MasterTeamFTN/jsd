import sys
from os import mkdir
from os.path import exists, dirname, join
import jinja2
from textx import metamodel_from_file

this_folder = dirname(__file__)

def get_mm():
    """
    Builds and returns a meta-model for our language.
    """
    return metamodel_from_file(join(this_folder, 'grammars', 'grammar.tx'))

def main(model_filename, debug=False):
    # Instantiate meta-model
    mm = get_mm()

    # Create the output folder
    srcgen_folder = join(this_folder, 'srcgen')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    # Initialize the template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    # Load template
    template_path = join('templates', 'sql_create.template')
    template = jinja_env.get_template(template_path)

    # Build a model from fakultet.sg file
    model = mm.model_from_file(model_filename)

    database_name = model.config.db_name

    # Generate SQL code
    with open(join(srcgen_folder, "create_db_schema.sql"), 'w') as f:
        f.write(template.render(entities=model.structures, database_name=database_name))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Enter file name as first parameter')
        exit(1)

    filename = sys.argv[1]
    print(f'File to interpret: {filename}')

    main(filename)
