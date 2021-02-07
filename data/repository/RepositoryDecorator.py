import sqlite3
import os

def fetch_request(statement:str):
    def wrap(func):
        def wrapped(*args):
            project_dir = os.getcwd()
            conn = sqlite3.connect(project_dir + "/data/db/py_tube.db")
            cursor = conn.execute(statement, [*args[1:]])
            result = func(cursor, *args[1:])
            conn.close()
            return result
        return wrapped
    return wrap

def insert_request(table:str):
    def wrap(func):
        def wrapped(*args):
            project_dir = os.getcwd()
            conn = sqlite3.connect(project_dir + "/data/db/py_tube.db")
            cursor = conn.execute("insert or ignore into " + table + " values " + func(*args))
            conn.commit()
            conn.close()
        return wrapped
    return wrap

def delete_request(table:str, appendage:str = None):
    def wrap(func):
        def wrapped(*args):
            project_dir = os.getcwd()
            conn = sqlite3.connect(project_dir + "/data/db/py_tube.db")
            statement = 'delete from ' + table + " " + appendage
            cursor = conn.execute(statement, [*args[1:]])
            result = func(cursor, *args[1:])
            conn.commit()
            conn.close()
            return result
        return wrapped
    return wrap

def update_request(table:str, appendage:str = None):
    def wrap(func):
        def wrapped(*args):
            project_dir = os.getcwd()
            conn = sqlite3.connect(project_dir + "/data/db/py_tube.db")
            statement = 'update ' + table + " " + appendage
            cursor = conn.execute(statement, [*args[1:]])
            result = func(cursor, *args[1:])
            conn.commit()
            conn.close()
            return result
        return wrapped
    return wrap

