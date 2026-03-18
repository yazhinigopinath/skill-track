"""
Database connection helper for Skill Track
Uses mysql-connector-python
"""

import mysql.connector
from mysql.connector import Error
from flask import current_app, g


def get_db():
    """Get or create a database connection for the current request."""
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB'],
                charset='utf8mb4',
                autocommit=False
            )
        except Error as e:
            current_app.logger.error(f"Database connection error: {e}")
            raise
    return g.db


def close_db(e=None):
    """Close database connection at end of request."""
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()


def query_db(sql, args=(), one=False, commit=False):
    """Execute a query and return results."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(sql, args)
        if commit:
            db.commit()
            return cursor.lastrowid
        rv = cursor.fetchall()
        return (rv[0] if rv else None) if one else rv
    except Error as e:
        if commit:
            db.rollback()
        raise e
    finally:
        cursor.close()


def init_app(app):
    """Register database teardown with Flask app."""
    app.teardown_appcontext(close_db)
