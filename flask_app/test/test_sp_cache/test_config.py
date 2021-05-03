"""Test our Solr config for sp_cache."""
import pysolr

from flask_app.sp_cache.config import COLLECTIONS_URL, SPECIMENS_URL

# .....................................................................................
def test_connect_to_collections_core():
    pysolr.Solr(COLLECTIONS_URL)


# .....................................................................................
def test_connect_to_specimens_core():
    pysolr.Solr(SPECIMENS_URL)
