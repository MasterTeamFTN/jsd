from setuptools import setup, find_packages

setup(
    name='JsdProject',
    version='0.1',
    author='Boris Sulicenko, Janko Ljubic, Nikolina Petrovic',
    author_email='boris.sulicenko@uns.ac.rs',
    packages=find_packages(),
    license='MIT',
    description='DSL that is used to generate SQL script and ER diagram',
    long_description=open('README.md').read(),
    install_required=[
        'textX==2.3.0',
        'Jinja2==2.11.2'
    ],
    entry_points={
        'textx_languages': [
            'jsd_language = sql_generator.main:jsd_lang',
        ],
        'textx_generators': [
            'sg_sql = sql_generator.main:sql_generator',
            'sg_dot = sql_generator.main:dot_generator'
        ],
    }
)
