"""Root Flask application for Syftorium."""
import os

from flask import Flask

import sp_cache


# .....................................................................................
def create_app(test_config=None):
    """Create a Flask application.

    Args:
        test_config (dict): Testing configuration parameters.

    Returns:
        Flask: Flask application.
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def syftorium_root():
        """Root endpoint for all services under syftorium umbrella.

        Returns:
            str: A string welcoming the user to the syftorium
        """
        return 'Welcome to the Syftorium!'

    app.register_blueprint(sp_cache.bp)

    return app
