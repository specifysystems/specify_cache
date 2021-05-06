import sys
sys.path.append('/state/partition1/lmscratch/git/syftorium-server/')

from flask_app.application import create_app
application = create_app()
