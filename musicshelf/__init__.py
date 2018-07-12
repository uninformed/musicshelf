import os
from flask import Flask, render_template
from flaskext.mysql import MySQL
#from werkzeug.security import generate_password_hash

def create_app(test_config=None):
    """
    Create and configure the application.

    :param test_config: configuration for testing
    :return: the Flask application
    """
    app = Flask(__name__, instance_relative_config=True)
    # the following is for temporary testing purposes
    app.config.from_mapping(
        SECRET_KEY='dev'    #TEMP
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import user
    app.register_blueprint(user.bp)

    from . import master
    app.register_blueprint(master.bp)

    @app.route('/')
    def index():
        """
        The index page: show the collection.
        """
        cursor = db.get_db().cursor()
        cursor.execute(
            'SELECT * FROM msmaster ORDER BY artist, year;'
        )
        masters = cursor.fetchall()
        return render_template('index.html', masters=masters)

    @app.route('/setup')
    def setup():
        """
        STUB: Walk the user through first-time setup.
        """
        return 'Not yet implemented!'

    @app.route('/hello')
    def hello():
        """
        Test page to ensure the server is working.
        """
        return 'Hello, World! The server is still working!'

    return app
