import sqlite3
from sqlite3 import Error as error_db
import os
import sys


def connectDb():
    try:
        database = 'unoesc.db.sqlite'
        if not os.path.exists(database):
            raise sqlite3.DatabaseError
        connection = sqlite3.connect(f'file:{database}?mode=rw', uri=True)
        return connection
    except sqlite3.DatabaseError as e:
        print("Banco de dados não existe")
        sys.exit()
    except error_db as e:
        print("não conectou")
        print(e)
        sys.exit()


def createTable(connection, table, attrs):
    strAttrs = ''
    for x in range(0, len(attrs)):
        if(x != len(attrs)-1):
            strAttrs += attrs[x][0] + " " + attrs[x][1] + ','
        else:
            strAttrs += attrs[x][0] + " " + attrs[x][1]

    strConnection = f"CREATE TABLE IF NOT EXISTS {table} ({strAttrs})"
    try:
        cursor = connection.cursor()
        cursor.execute(strConnection)
        connection.commit()
    except error_db as e:
        print(e)
    finally:
        if connection:
            connection.close()


def get_columns(connection, table):
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    registros = cursor.fetchall()
    colunas = []
    for registro in registros:
        colunas.append([registro[1], registro[2]])
    return colunas

def get_tables(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    registros = cursor.fetchall()

    return registros

def selectQueryDb(connection, table, params):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT {params} FROM {table}")
        registros = cursor.fetchall()
        return registros
    except error_db as e:
        print("error")
        print(e)
    finally:
        if connection:
            connection.close()


def queryDbCommit(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except error_db as e:
        print("error")
        print(e)
    finally:
        if connection:
            connection.close()


def insertDbCommit(connection, table, labelsToInsert, valuesToInsert):
    strLabel = ''
    strValues = ''
    for x in range(0, len(labelsToInsert)):
        if(x != len(labelsToInsert)-1):
            strLabel += labelsToInsert[x][0] + ', '
        else:
            strLabel += labelsToInsert[x][0]

    for x in range(0, len(valuesToInsert)):
        col = labelsToInsert[x][1].upper()
        if(x != len(valuesToInsert)-1):
            if(col == "NUMBER" or col == "INTEGER" or col == "FLOAT" or col == "DOUBLE"):
                strValues += valuesToInsert[x] + ', '
            else:
                # print(labelsToInsert[x][1].upper())
                strValues += f"'{valuesToInsert[x]}'" + ', '
        else:
            if(col == "NUMBER" or col == "INTEGER" or col == "FLOAT" or col == "DOUBLE"):
                strValues += valuesToInsert[x]
            else:
                strValues += f"'{valuesToInsert[x]}'"
    try:
        cursor = connection.cursor()
        strSQL = f'INSERT INTO {table} ({strLabel}) VALUES ({strValues})'
        cursor.execute(strSQL)
        connection.commit()
    except error_db as e:
        print("error")
        print(e)
    finally:
        if connection:
            connection.close()


def updateDbCommit(connection, table, value, where):
    try:
        if(type(value[1]) != int):
            value[1] = f'"{value[1]}"'
        if(type(where[1]) != int):
            where[1] = f'"{where[1]}"'
        cursor = connection.cursor()
        strSQL = f'UPDATE {table} set {value[0]}={value[1]} WHERE ({where[0]} = {where[1]})'
        cursor.execute(strSQL)
        connection.commit()
    except error_db as e:
        print(e)
    finally:
        if connection:
            connection.close()


def deleteDbCommit(connection, table, where):
    try:
        if(type(where[1]) != int):
            where[1] = f'"{where[1]}"'
        cursor = connection.cursor()

        strSQL = f'DELETE FROM {table} WHERE {where[0]}= {where[1]}'
        cursor.execute(strSQL)
        connection.commit()
        print("Deletado!")
    except error_db as e:
        print(e)
    finally:
        if connection:
            connection.close()