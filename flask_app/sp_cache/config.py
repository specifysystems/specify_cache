"""Solr configuration parameters."""

SOLR_SERVER = 'http://localhost'
SOLR_PORT = 8983

COLLECTIONS_URL = '{}:{}/solr/sp_collections'.format(SOLR_SERVER, SOLR_PORT)
SPECIMENS_URL = '{}:{}/solr/specimen_records'.format(SOLR_SERVER, SOLR_PORT)
