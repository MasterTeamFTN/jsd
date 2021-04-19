from distutils.core import setup

setup(
    name='JsdProject',
    version='0.1dev',
    packages=['sql_generator', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),

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
