from template_engine import mysql, postgresql

def get_type(name, database):
    if database == "mysql":
        return mysql(name)
    elif database == "postgresql":
        return postgresql(name)

constraints = {
    'pk': 'PRIMARY KEY',
    'notnull': 'NOT NULL',
    'unique': 'UNIQUE'
}
