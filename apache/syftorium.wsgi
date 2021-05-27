import sys
sys.path.append('/opt/lifemapper/')

from flask_app.application import create_app  # noqa: E402
application = create_app()
