import sqlite3
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            os.path.join(current_app.root_path, 'app.db'),
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """
    Closes the database again at the end of the request.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """
    Initializes the database with a schema.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def insert_item(name, description, image_filename):
    """
    Inserts a new item into the database.
    """
    db = get_db()
    db.execute(
        'INSERT INTO items (name, description, image_filename) VALUES (?, ?, ?)',
        (name, description, image_filename)
    )
    db.commit()

def get_items():
    """
    Fetches all items from the database.
    """
    db = get_db()
    items = db.execute('SELECT * FROM items').fetchall()
    return items

@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Clears the existing data and creates new tables.
    """
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """
    Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
