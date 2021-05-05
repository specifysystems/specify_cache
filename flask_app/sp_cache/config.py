"""Solr configuration parameters."""
import os

SOLR_SERVER = 'http://localhost'
SOLR_PORT = 8983

COLLECTIONS_URL = '{}:{}/solr/sp_collections'.format(SOLR_SERVER, SOLR_PORT)
SPECIMENS_URL = '{}:{}/solr/specimen_records'.format(SOLR_SERVER, SOLR_PORT)

BACKUP_DATA_PATH = '/state/partition2/syftorium_data/'
COLLECTION_BACKUP_PATH = os.path.join(BACKUP_DATA_PATH, 'collections')
DWCA_PATH = os.path.join(BACKUP_DATA_PATH, 'new_dwcas')
