"""
Most of this adapted from the Flask SQLite documentation:
https://flask.palletsprojects.com/en/2.2.x/patterns/sqlite3/

"""
import sqlite3
from flask import g
from . import utils


def _get_db():
    # open a database connection if there isn't one already
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(utils.DATABASE_PATH)
        db.row_factory = _make_dicts
    return db


def _make_dicts(cursor, row):
    """function to use the DB row names to create a dict from the results"""
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def execute_update(statement, args=()):
    """executes the given statement (insert or update)"""
    cur = _get_db()
    cur.execute(statement, args)
    cur.commit()


def execute_query(query, args=(), one=False):
    """execute the given SQL query and return the results

    :param query: the sql query
    :param args: arguments to fill in "?" syntax in the query
    :param one: True/False value, if True it will return only the first result from the query
    """
    cur = _get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
