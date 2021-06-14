"""Solr configuration parameters."""
import os

from lmsyft.flask_app.config.constants import BACKUP_DATA_PATH, SOLR_PORT, SOLR_SERVER


COLLECTIONS_URL = '{}:{}/solr/sp_collections'.format(SOLR_SERVER, SOLR_PORT)
SPECIMENS_URL = '{}:{}/solr/specimen_records'.format(SOLR_SERVER, SOLR_PORT)

COLLECTION_BACKUP_PATH = os.path.join(BACKUP_DATA_PATH, 'collections')
DWCA_PATH = os.path.join(BACKUP_DATA_PATH, 'new_dwcas')
PROCESSED_DWCA_PATH = os.path.join(BACKUP_DATA_PATH, 'processed_dwcas')