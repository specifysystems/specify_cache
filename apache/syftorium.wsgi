import sys
sys.path.append('/opt/lifemapper/')

from lmsyft.flask_app.application import create_app  # noqa: E402
application = create_app()
