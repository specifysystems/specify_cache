"""Solr configuration parameters."""
from lmsyft.flask_app.config.constants import SOLR_PORT, SOLR_SERVER

RESOLVER_URL = '{}:{}/solr/spcoco'.format(SOLR_SERVER, SOLR_PORT)
