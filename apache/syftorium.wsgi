import sys
sys.path.append('/opt/lifemapper/')

from flask_app.application import create_app
application = create_app()
