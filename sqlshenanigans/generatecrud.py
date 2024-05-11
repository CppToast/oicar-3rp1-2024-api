import definitions

def generate_table_creation_sql(table_name, columns):
    sql = f"CREATE TABLE {table_name} (\n"
    for column in columns:
        col_name, data_type, constraints = column
        sql += f"    {col_name} {data_type}"
        if constraints:
            sql += f" {' '.join(constraints)}"
        sql += ",\n"
    sql = sql.rstrip(",\n") + "\n);"
    return sql

def generate_insert_procedure(table_name, columns):
    primary_key = None
    for column in columns:
        col_name, data_type, constraints = column
        if 'PRIMARY KEY' in constraints:
            primary_key = col_name
            break
    
    if not primary_key:
        raise ValueError("Primary key column not found.")
    
    parameters = ", ".join([f"@{col[0]} {col[1]}" for col in columns if col[0] != primary_key])
    insert_sql = f"""
CREATE PROCEDURE Insert{table_name}
    {parameters}
AS
BEGIN
    INSERT INTO {table_name} ({', '.join([col[0] for col in columns if col[0] != primary_key])})
    VALUES ({', '.join([f'@{col[0]}' for col in columns if col[0] != primary_key])});
END;
"""
    return insert_sql

def generate_select_procedure(table_name):
    select_sql = f"""
CREATE PROCEDURE Select{table_name}
AS
BEGIN
    SELECT * FROM {table_name};
END;
"""
    return select_sql

def generate_update_procedure(table_name, columns):
    primary_key = None
    for column in columns:
        col_name, data_type, constraints = column
        if 'PRIMARY KEY' in constraints:
            primary_key = col_name
            break
    
    if not primary_key:
        raise ValueError("Primary key column not found.")
    
    update_sql = f"""
CREATE PROCEDURE Update{table_name}
    @{primary_key} {columns[0][1]},
    {', '.join([f'@{col[0]} {col[1]}' for col in columns if col[0] != primary_key])}
AS
BEGIN
    UPDATE {table_name}
    SET {', '.join([f'{col[0]} = @{col[0]}' for col in columns if col[0] != primary_key])}
    WHERE {primary_key} = @{primary_key};
END;
"""
    return update_sql

def generate_delete_procedure(table_name, columns):
    primary_key = None
    for column in columns:
        col_name, data_type, constraints = column
        if 'PRIMARY KEY' in constraints:
            primary_key = col_name
            break
    
    if not primary_key:
        raise ValueError("Primary key column not found.")
    
    delete_sql = f"""
CREATE PROCEDURE Delete{table_name}
    @{primary_key} {columns[0][1]}
AS
BEGIN
    DELETE FROM {table_name} WHERE {primary_key} = @{primary_key};
END;
"""
    return delete_sql



lines = []

lines.append(f"USE master\n")
lines.append(f"DROP DATABASE IF EXISTS {definitions.database_name}\n")
lines.append(f"GO\n")
lines.append(f"CREATE DATABASE {definitions.database_name}\n")
lines.append(f"GO\n")
lines.append(f"USE {definitions.database_name}\n")

for table in definitions.tables:
    table_name = table.name
    columns = table.columns

    table_creation_sql = generate_table_creation_sql(table_name, columns)
    insert_procedure_sql = generate_insert_procedure(table_name, columns)
    select_procedure_sql = generate_select_procedure(table_name)
    update_procedure_sql = generate_update_procedure(table_name, columns)
    delete_procedure_sql = generate_delete_procedure(table_name, columns)

    lines.append(f"--{table_name}")

    lines.append("\n--Table Creation SQL:\n")
    lines.append(table_creation_sql)
    lines.append("\nGO\n")
    lines.append("\n--CRUD Operations SQL:\n")
    lines.append(insert_procedure_sql)
    lines.append("\nGO\n")
    lines.append(select_procedure_sql)
    lines.append("\nGO\n")
    lines.append(update_procedure_sql)
    lines.append("\nGO\n")
    lines.append(delete_procedure_sql)
    lines.append("\nGO\n")

outfile = open("out.sql", "w")
outfile.writelines(lines)
outfile.close()