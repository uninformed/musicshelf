from flaskext.mysql import MySQL
import pymysql.cursors
from flask import current_app, g
from flask.cli import with_appcontext
import click

def get_db():
    """
    Initialize and return a connection to the database.

    :return: db connection object
    """
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASS'],
            db=current_app.config['MYSQL_DB'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

def close_db(e=None):
    """
    Close the connection to the database.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """
    Add ``close_db()`` to the teardown code and ``init_db()`` as
    a cli command.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
