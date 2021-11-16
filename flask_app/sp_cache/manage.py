from flask.cli import FlaskGroup

from flask_app.sp_cache import app

cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()