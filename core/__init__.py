import mysql.connector
from datetime import datetime
from core.layouts import mainl, seedmainl
from core.datatype import datatype
import os
import re
from core import helper


def generate_migration(host, port, user, password, database_name, path):
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../{}".format(path))
    else:
        path = os.path.join(path, "migrations")
    if not os.path.exists(path):
        os.makedirs(path, 777, True)
    mydb = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password if password else "",
        database=database_name
    )
    tableCursor = mydb.cursor()
    tableCursor.execute("show tables")
    tables = tableCursor.fetchall()
    reference = {}
    for table in tables:
        table = table[0]
        currentfiletime = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "{}/{}-create-{}.js".format(path, currentfiletime, table)
        query = "SELECT COLUMN_NAME,DATA_TYPE,COLUMN_TYPE,COLUMN_DEFAULT,IS_NULLABLE,CHARACTER_MAXIMUM_LENGTH,COLUMN_KEY," \
                "EXTRA,COLUMN_COMMENT FROM information_schema.COLUMNS WHERE TABLE_NAME = '{}' AND TABLE_SCHEMA='{" \
                "}'".format(table, database_name)

        desccur = mydb.cursor(dictionary=True)
        desccur.execute(query)
        columns = desccur.fetchall()
        definition = []
        for column in columns:
            column_name = helper.columnName(column['COLUMN_NAME'])
            data_type = datatype[column['DATA_TYPE']]
            if column['DATA_TYPE'] == "enum":
                enum_val = '", "'.join(re.split('enum\(\'|\',\'|\'\)', column['COLUMN_TYPE'])[1:-1])
                data_type = datatype["enum"]
            if column['DATA_TYPE'] == "varchar" and int(column['CHARACTER_MAXIMUM_LENGTH']) < 255:
                data_type = "{}({})".format(data_type, column['CHARACTER_MAXIMUM_LENGTH'])
            defs = '''\n
            {}:{obras}
                type: {},
            '''.format(helper.columnName(column['COLUMN_NAME']), data_type, obras="{")
            if column['IS_NULLABLE'] == "YES":
                defs += "\tallowNull: true,\n"
            else:
                defs += "\tallowNull: false,\n"
            if column['COLUMN_KEY'] == "PRI":
                defs += "\t\t\tprimaryKey: true,\n"
            if column['COLUMN_KEY'] == "UNI":
                defs += "\t\t\tunique: true,\n"
            if column['EXTRA'] == "auto_increment":
                defs += "\t\t\tautoIncrement: true,\n"
            if column['DATA_TYPE'] == "enum":
                defs += "\t\t\tvalues: [\"{}\"],\n".format(enum_val)

            if column['COLUMN_KEY'] == "MUL":
                query_check_foren_key = "SELECT i.TABLE_NAME, i.CONSTRAINT_TYPE, i.CONSTRAINT_NAME, " \
                                        "k.REFERENCED_TABLE_NAME, k.REFERENCED_COLUMN_NAME, k.COLUMN_NAME FROM " \
                                        "information_schema.TABLE_CONSTRAINTS i LEFT JOIN " \
                                        "information_schema.KEY_COLUMN_USAGE k ON i.CONSTRAINT_NAME = k.CONSTRAINT_NAME " \
                                        "WHERE i.TABLE_SCHEMA = '{}' AND " \
                                        "i.TABLE_NAME = '{}' AND k.COLUMN_NAME ='{}'".format(database_name, table,
                                                                                             column['COLUMN_NAME'])
                check_key = mydb.cursor(dictionary=True, buffered=True)
                check_key.execute(query_check_foren_key)
                key = check_key.fetchone()
                if key:
                    # if not helper.checkReferenceTableCreated(key['REFERENCED_TABLE_NAME']):
                    reference[key['REFERENCED_TABLE_NAME']] = currentfiletime
                    defs += "\t\t\treferences:{ \n\t\t\t\tmodel:'" + key[
                        'REFERENCED_TABLE_NAME'] + "',\n\t\t\t\tkey:'" + \
                            key['REFERENCED_COLUMN_NAME'] + "'\n\t\t\t}\n"

            defs += "\t\t}"
            definition.append(defs)

        definition = ",".join(definition)
        main_layout = mainl.format(definition=definition, table_name=table, obras="{", cbras="\n\t}")
        file = open(file_name, 'w')
        file.write(main_layout)
        file.close()
        print("Migration Generated : {}".format(file_name))
    for table, time in reference.items():
        helper.renameReferenceTableMigration(table, time)


# check_key = mydb.cursor(dictionary=True)
# check_key.execute(query_check_foren_key)
# desc = check_key.fetchall()
# print(main_layout)

def generate_seeds(host, port, user, password, database_name, path):
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../seeds")
    else:
        path = os.path.join(path, "seeds")
    if not os.path.exists(path):
        os.makedirs(path, 777, True)
    mydb = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password if password else "",
        database=database_name
    )
    tableCursor = mydb.cursor()
    tableCursor.execute("show tables")
    tables = tableCursor.fetchall()
    for table in tables:
        table = table[0]
        if table == "sequelizemeta":
            continue
        currentfiletime = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "{}/{}-create-{}.js".format(path, currentfiletime, table)
        query = "SELECT * FROM `{}`".format(table)

        desccur = mydb.cursor(dictionary=True)
        desccur.execute(query)
        datas = desccur.fetchall()
        definition = []
        for data in datas:
            if data is not None:
                l = '''\n\t\t\t\t{'''
                for colunm, d in data.items():
                    if colunm not in ["createdAt", "updatedAt"]:
                        l += "\n\t\t\t\t\t{}: '{}',".format(colunm, d)
                l += '''\n\t\t\t\t}'''
                definition.append(l)
        if len(definition):
            definition = ",".join(definition)
            main_layout = seedmainl.format(definition=definition, table_name=table, obras="{", cbras="}")
            file = open(file_name, 'w',encoding="utf8")
            file.write(main_layout)
            file.close()
            print("Migration Generated : {}".format(file_name))
