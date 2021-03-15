from os.path import join
import jinja2

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
    # return jinja_env.get_template(template_path)
    return jinja_env.get_template('templates/' + template_name)
