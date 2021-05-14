"""Solr configuration parameters."""
import os

SOLR_SERVER = 'http://localhost'
SOLR_PORT = 8983

RESOLVER_URL = '{}:{}/solr/spcoco'.format(SOLR_SERVER, SOLR_PORT)
