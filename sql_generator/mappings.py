from template_engine import mysql, postgresql

def get_type(name, database):
    if 'CustomType' in name._tx_fqn:
        if exists_in_database(name.value.lower(), database):
            return name.value.upper()
        else:
            print("Custom type not valid")
            exit(1)

    if database == "mysql":
        return mysql(name)
    elif database == "postgresql":
        return postgresql(name)


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
