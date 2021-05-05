"""Flask functions for Specify Cache."""
import json
import os

from flask import Blueprint
from werkzeug.exceptions import NotFound

from . import config as config
from . import models as models
from . import solr_controller as controller


bp = Blueprint('sp_cache', __name__, url_prefix='/sp_cache')


# .....................................................................................
@bp.route('/', methods=['GET'])
def sp_cache_status():
    """Get overall health of the cache.

    Returns:
        dict: A dictionary of status information for the server.
    """
    num_collections = 0
    num_records = 0
    system_status = 'In Development'
    return {
        'num_collections': num_collections,
        'num_records': num_records,
        'status': system_status
    }



# .....................................................................................
@bp.route('/collection', methods=['POST'])
def sp_cache_collection_post():
    """Post a new collection to the cache.

    Returns:
        dict: Collection information in dictionary format (JSON).
    """
    collection = models.Collection(request.json)
    controller.post_collection(collection)
    # Write collection information backup file
    collection_id = collection.attributes['collection_id']
    collection_filename = os.path.join(
        config.COLLECTION_BACKUP_PATH, '{}.json'.format(collection_id)
    )
    with open(collection_filename, mode='wt') as out_json:
        json.dump(request.json, out_json)
    return controller.get_collection(collection_id).serialize_json()


# .....................................................................................
@bp.route('/collection/<string:collection_id>', methods=['GET'])
def sp_cache_collection_get(collection_id):
    """Return information about a cached collection.

    Args:
        collection_id (str): An identifier for the collection to retrieve.

    Returns:
        dict: Collection information in JSON format.

    Raises:
        NotFound: Raised if the collection is not found.
    """
    collection = controller.get_collection(collection_id)
    if collection:
        return collection.serialize_json()
    raise NotFound()


# .....................................................................................
@bp.route(
    '/collection/<string:collection_id>/occurrences/',
    methods=['DELETE', 'POST', 'PUT']
)
def collection_occurrences_modify(collection_id):
    """Modify collection specimen holdings.

    Args:
        collection_id (str): An identifier associated with these specimens.
    """
    if request.method.lower() in ['post', 'put']:
        # Write data to file system for another process to pick up and handle
        date_string = 'YY_MM_DD_HH_MM_SS'
        dwca_filename = os.path.join(
            config.DWCA_PATH, 'collection-{}-{}-{}'.format(
                collection_id, request.method.lower(), date_string
            )
        )
        with open(dwca_filename, mode='wb') as dwca_out:
            dwca_out.write(request.data)
    elif request.method.lower() == 'delete':
        delete_identifiers = request.json['delete_identifiers']
        controller.delete_collection_occurrences(collection_id, delete_identifiers)


# .....................................................................................
@bp.route(
    '/collection/<string:collection_id>/occurrences/<string:identifier>',
    methods=['DELETE', 'GET', 'PUT']
)
def collection_occurrence(collection_id, identifier):
    """Retrieve a specimen record.

    Args:
        collection_id (str): An identifer for the collection holding this specimen.
        identifier (str): An identifier for the specimen to retrieve.

    Returns:
        dict: Returned if the specimen is found and requested to retrieve (GET).
        None: Returned if the specimen is found and deleted (DELETE).

    Raises:
        NotFound: Raised if the desired specimen is not found.
    """
    if request.method.lower() == 'delete':
        return controller.delete_collection_occurrences(collection_id, [identifier])
    elif request.method.lower() == 'get':
        specimen = controller.get_specimen(collection_id, identifier)
        if specimen:
            return specimen.serialize_json()
        raise NotFound()
    elif request.method.lower() == 'put':
        new_specimen_record = models.SpecimenRecord(request.json)
        controller.update_collection_occurrences(collection_id, [new_specimen_record])
        return controller.get_specimen(collection_id, identifier).serialize_json()
