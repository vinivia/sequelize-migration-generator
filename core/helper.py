import glob
import os


def checkReferenceTableCreated(table_name):
    filename = "migrations/*-create-{}.js".format(table_name)
    file = glob.glob(filename)
    return len(file) == 1


def renameReferenceTableMigration(table_name, current_file):
    current_file = str(int(current_file) - 5)
    newfilename = "migrations/{}-create-{}.js".format(current_file, table_name)
    filename = "migrations/*-create-{}.js".format(table_name)
    file = glob.glob(filename)
    if len(file) > 0:
        os.rename(file[0], newfilename)


def columnName(column):
    if column == "organizationId":
        column = "tenantId"
    return column
