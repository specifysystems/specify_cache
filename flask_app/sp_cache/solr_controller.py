"""Solr backend controller module for Specify Cache."""
import csv

from models import Collection, SpecimenRecord

# Need an easy way to get solr classes
# Try using results_cls parameter to get and post proper results

# .....................................................................................
def post_collection(collection):
    solr.add(collection)


# .....................................................................................
def get_collection(collection_id):
    return solr.search('q=collection_id:{}'.format(collection_id))


# .....................................................................................
def update_collection(collection):
    solr.update(collection)


# .....................................................................................
def get_summary():
    pass


# .....................................................................................
def delete_collection(collection_id):
    solr.delete('q=collection_id:{}'.format(collection_id))


# .....................................................................................
def update_collection_occurrences(collection_id, specimens):
    solr.add(specimens)


# .....................................................................................
def delete_collection_occurrences(collection_id, identifiers):
    solr.delete(
        'q=collection_id:{},identifier={}'.format(collection_id, ','.join(identifiers))
    )


# .....................................................................................
def get_specimen(collection_id, identifier):
    rec = solr.search(
        'q=collection_id:{},identiifer:{}'.format(collection_id, identifier)
    )
    return SpecimenRecord(rec)


# .....................................................................................
def process_occurrence_dca(collection_id, dca_file, meta_filename, data_filename):
    """Process a Specify export."""
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
                solr.add([rec.serialize_json() for rec in specimens_to_post])
                specimens_to_post = []
        # Add any leftover to solr
        if len(specimens_to_post) > 0:
            solr.add([rec.serialize_json() for rec in specimens_to_post])
    