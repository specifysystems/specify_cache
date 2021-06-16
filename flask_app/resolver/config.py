"""Solr configuration parameters."""
from lmsyft.config.constants import SOLR_PORT, SOLR_SERVER

RESOLVER_URL = '{}:{}/solr/spcoco'.format(SOLR_SERVER, SOLR_PORT)

ARK_PATTERN = 'http://spcoco.org/ark:/<guid>'
