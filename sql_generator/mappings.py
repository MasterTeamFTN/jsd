def get_type(name, database):
    value = name.value if 'CustomType' in name._tx_fqn else name.name

    if exists_in_database(value.lower(), database):
        value = checkMysqlVarchar(database, value.upper())
        return value.upper()
    else:
        checked_value = check_common_types(value, database)
        if  checked_value != value:
            return checked_value
        else:
            print("Custom type not valid")
            exit(1)

constraints = {
    'pk': 'PRIMARY KEY',
    'notnull': 'NOT NULL',
    'unique': 'UNIQUE'
}

def exists_in_database(value, database):
    if database == "mysql":
        return value in (ms.lower() for ms in mysql_types)
    elif database == "postgresql":
        return value in (ps.lower() for ps in psql_types)
    else:
        return False

def checkMysqlVarchar(database, value):
    if database == "mysql":
        if value == "VARCHAR":
            return "VARCHAR(255)"
    return value

psql_types = [
    'bigint',
    'bigserial',
    'bit',
    'bit varying',
    'varbit',
    'boolean',
    'box',
    'bytea',
    'character',
    'char',
    'varchar',
    'cidr',
    'circle',
    'date',
    'double precision',
    'float8',
    'inet',
    'integer',
    'int',
    'int4',
    'interval',
    'json',
    'jsonb',
    'line',
    'lseg',
    'macaddr',
    'money',
    'numeric',
    'decimal',
    'path',
    'pg_lsn',
    'point',
    'polygon',
    'real',
    'float4',
    'smallint',
    'int2',
    'smallserial',
    'serial2',
    'serial',
    'serial4',
    'text',
    'time',
    'timetz',
    'timestamp',
    'timestamptz',
    'tsquery',
    'tsvector',
    'txid_snapshot',
    'uuid',
    'xml'
]

mysql_types = [
    'CHAR',
    'VARCHAR',
    'TINY',
    'TEXT',
    'BLOB',
    'MEDIUMTEXT',
    'MEDIUMBLOB',
    'LONGTEXT',
    'LONGBLOB',
    'TINYINT',
    'SMALLINT',
    'MEDIUMINT',
    'INT',
    'BIGINT',
    'FLOAT',
    'DOUBLE',
    'DECIMAL',
    'DATE',
    'DATETIME',
    'TIMESTAMP',
    'TIME',
    'ENUM',
    'SET',
    'BOOLEAN'
]

def check_common_types(value, database):
    if database == "mysql":
        return mysql(value)
    elif database == "postgresql":
        return postgresql(value)

def mysql(s):
    return {
        'integer': 'INT UNSIGNED',
        'string': 'VARCHAR(255)',
        'char': 'CHAR'
    }.get(s, s)

def postgresql(s):
    return {
        'integer': 'INTEGER',
        'string': 'VARCHAR',
        'float': 'REAL'
    }.get(s, s)

#
# def mysql(s):
#     return {
#             'integer': 'INT UNSIGNED',
#             'string': 'VARCHAR(255)',
#             'char': 'CHAR',
#             'varchar': 'VARCHAR(255)',
#             'tiny': 'TINY',
#             'text': 'TEXT',
#             'blob': 'BLOB',
#             'medumtext': 'MEDIUMTEXT',
#             'mediumblob': 'MEDIUMBLOB',
#             'longtext': 'LONGTEXT',
#             'longblob': 'LONGBLOB',
#             'tinyint': 'TINYINT',
#             'smallint': 'SMALLINT',
#             'mediumint': 'MEDIUMINT',
#             'int': 'INT',
#             'bigint': 'BIGINT',
#             'float': 'FLOAT',
#             'double': 'DOUBLE',
#             'decimal': 'DECIMAL',
#             'date': 'DATE',
#             'datetime': 'DATETIME',
#             'timestamp': 'TIMESTAMP',
#             'time': 'TIME',
#             'enum': 'ENUM',
#             'set': 'SET',
#             'boolean': 'BOOLEAN'
#     }.get(s.name, s.name)
#
# def postgresql(s):
#     return {
#             'integer': 'INTEGER',
#             'string': 'VARCHAR',
#             'float': 'REAL',
#                'bigint': 'bigint',
#            'bigserial': 'bigserial',
#            'bit': 'bit',
#            'bit varying': 'bit varying',
#            'varbit': 'varbit',
#            'boolean': 'boolean',
#            'box': 'box',
#            'bytea': 'bytea',
#            'character': 'character',
#            'char': 'char',
#            'varchar': 'varchar',
#            'cidr': 'cidr',
#            'circle': 'circle',
#            'date': 'date',
#            'double precision': 'double precision',
#            'float8': 'float8',
#            'inet': 'inet',
#            'integer': 'integer',
#            'int': 'int',
#            'int4': 'int4',
#            'interval': 'interval',
#            'json': 'json',
#            'jsonb': 'jsonb',
#            'line': 'line',
#            'lseg': 'lseg',
#            'macaddr': 'macaddr',
#            'money': 'money',
#            'numeric': 'numeric',
#            'decimal': 'decimal',
#            'path': 'path',
#            'pg_lsn': 'pg_lsn',
#            'point': 'point',
#            'polygon': 'polygon',
#            'real': 'real',
#            'float4': 'float4',
#            'smallint': 'smallint',
#            'int2': 'int2',
#            'smallserial': 'smallserial',
#            'serial2': 'serial2',
#            'serial': 'serial',
#            'serial4': 'serial4',
#            'text': 'text',
#            'time': 'time',
#            'timetz': 'timetz',
#            'timestamp': 'timestamp',
#            'timestamptz': 'timestamptz',
#            'tsquery': 'tsquery',
#            'tsvector': 'tsvector',
#            'txid_snapshot': 'txid_snapshot',
#            'uuid': 'uuid',
#            'xml': 'xml'
#     }.get(s.name, s.name)