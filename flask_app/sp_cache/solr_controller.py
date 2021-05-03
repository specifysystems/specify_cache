"""Solr backend controller module for Specify Cache."""
import csv
import pysolr

from .config import COLLECTIONS_URL, SPECIMENS_URL
from .models import Collection, SpecimenRecord


# Need an easy way to get solr classes
# Try using results_cls parameter to get and post proper results

# .....................................................................................
def get_collection_solr():
    """Get solr connection to collections core.

    Todo:
        Incorporate this into flask better.
    """
    return pysolr.Solr(COLLECTIONS_URL)


# .....................................................................................
def get_specimen_solr():
    """Get solr connection to specimens core.

    Todo:
        Incorporate this into flask better.
    """
    return pysolr.Solr(SPECIMENS_URL)


# .....................................................................................
def post_collection(collection):
    collection_solr = get_collection_solr()
    collection_solr.add(collection)


# .....................................................................................
def get_collection(collection_id):
    collection_solr = get_collection_solr()
    return collection_solr.search(collection_id)


# .....................................................................................
def update_collection(collection):
    collection_solr = get_collection_solr()
    collection_solr.update(collection)


# .....................................................................................
def get_summary():
    pass


# .....................................................................................
def delete_collection(collection_id):
    collection_solr = get_collection_solr()
    collection_solr.delete('q=collection_id:{}'.format(collection_id))


# .....................................................................................
def update_collection_occurrences(collection_id, specimens):
    sp_solr = get_specimen_solr()
    sp_solr.add(specimens)


# .....................................................................................
def delete_collection_occurrences(collection_id, identifiers):
    sp_solr = get_specimen_solr()
    sp_solr.delete(
        'q=collection_id:{},identifier={}'.format(collection_id, ','.join(identifiers))
    )


# .....................................................................................
def get_specimen(collection_id, identifier):
    sp_solr = get_specimen_solr()
    rec = sp_solr.search(
        'q=collection_id:{},identiifer:{}'.format(collection_id, identifier)
    )
    return SpecimenRecord(rec)


# .....................................................................................
def process_occurrence_dca(collection_id, dca_file, meta_filename, data_filename):
    """Process a Specify export."""
    sp_solr = get_specimen_solr()
    # Open zip file if necessary

    # Metadata
    meta_file = dca_file.extract(meta_filename)
    translate_dict = {}
    # Open data file
    specimens_to_post = []
    with open(data_filename) as data_file:
        # Open csv reader
        reader = csv.reader(data_file, headers=True)
        for row in reader:
            # Create object for each record
            specimens_to_post.append(SpecimenRecord.from_row(translate_dict, row))
            # If we reach a limit, post and reset
            if len(specimens_to_post) >= POST_SIZE_LIMIT:
                sp_solr.add([rec.serialize_json() for rec in specimens_to_post])
                specimens_to_post = []
        # Add any leftover to solr
        if len(specimens_to_post) > 0:
            sp_solr.add([rec.serialize_json() for rec in specimens_to_post])
    
