"""Test Solr functions."""
import sp_cache.solr_controller as app_solr

# .....................................................................................
def test_get_collection_solr():
    """Test that a collection core connection can be made."""
    _ = app_solr.get_collection_solr()


# .....................................................................................
def test_get_specimen_solr():
    """Test that a specimen core connection can be made."""
    _ = app_solr.get_specimen_solr()


# .....................................................................................
def test_post_get_delete_collection():
    collection_id = 'test_collection'
    collection_data = {
        'collection_id': collection_id,
        'institution_name': 'test institution',
        'last_updated': '2021-05-03T11:06:00Z',
        'public_key': 'specify_pub_key',
        'collection_location': 'Specify HQ',
        'contact_name': 'Test User',
        'contact_email': 'test@sfytorium.org',
    }
    app_solr.post_collection(collection_data)
    ret_col = app_solr.get_collection(collection_id)
    app_solr.delete_collection(collection_id)
    ret_col_2 = app_solr.get_collection(collection_id)

# .....................................................................................
#def update_collection(collection):
#    collection_solr = get_collection_solr()
#    collection_solr.update(collection)
#
#
# .....................................................................................
#def get_summary():
#    pass
#
#
# .....................................................................................
#def delete_collection(collection_id):
#    collection_solr = get_collection_solr()
#    collection_solr.delete('q=collection_id:{}'.format(collection_id))
##

# .....................................................................................
#def update_collection_occurrences(collection_id, specimens):
#    sp_solr = get_specimen_solr()
#    sp_solr.add(specimens)


# .....................................................................................
#def delete_collection_occurrences(collection_id, identifiers):
#    sp_solr = get_specimen_solr()
#    sp_solr.delete(
#        'q=collection_id:{},identifier={}'.format(collection_id, ','.join(identifiers))
#    )


# .....................................................................................
#def get_specimen(collection_id, identifier):
#    sp_solr = get_specimen_solr()
#    rec = sp_solr.search(
#        'q=collection_id:{},identiifer:{}'.format(collection_id, identifier)
#    )
#    return SpecimenRecord(rec)


# .....................................................................................
#def process_occurrence_dca(collection_id, dca_file, meta_filename, data_filename):
#    """Process a Specify export."""
#    sp_solr = get_specimen_solr()
#    # Open zip file if necessary
#
#    # Metadata
#    meta_file = dca_file.extract(meta_filename)
#    translate_dict = {}
#    # Open data file
#    specimens_to_post = []
#    with open(data_filename) as data_file:
#        # Open csv reader
#        reader = csv.reader(data_file, headers=True)
#        for row in reader:
#            # Create object for each record
#            specimens_to_post.append(SpecimenRecord.from_row(translate_dict, row))
#            # If we reach a limit, post and reset
#            if len(specimens_to_post) >= POST_SIZE_LIMIT:
#                sp_solr.add([rec.serialize_json() for rec in specimens_to_post])
#                specimens_to_post = []
#        # Add any leftover to solr
#        if len(specimens_to_post) > 0:
#            sp_solr.add([rec.serialize_json() for rec in specimens_to_post])
    
def test_post_get_delete_specimen():
    """Test various specimen operations."""
    collection_id = 'test_collection'
    known_identifier = 'bae4b1f5-df83-4183-8b6e-005abc5d97ad'
    test_filename = '../../test_data/dwc_update.zip'
    with open(test_filename, mode='rb') as in_file:
        solr_app.process_occurrence_dca(collection_id, in_file, meta_filename)
    rec = solr_app.get_specimen(collection_id, known_identifier)
    solr_app.delete_collection_occurrences(collection_id, [known_identifier])
 