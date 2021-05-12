"""Flask route definitions for the resolver."""
from flask import Blueprint, request

import controller as controller

OCCURRENCE_ID_QUERY_PARAMETER = 'occid'
PROVIDER_QUERY_PARAMETER = 'provider'

bp = Blueprint('resolve', __name__, url_prefix='/resolve')


# .....................................................................................
@bp.route('/', methods=['GET'])
def resolver_get():
    """Get zero or one record from the resolution service du jour.

    Get zero or one record for an identifier from the resolution service du jour
    (DOI, ARK, etc) or get a count of all records indexed by this resolution service.

    Returns:
        dict - A dictionary of metadata and a count of records found in GBIF and an
            optional list of records.

    Note:
        There will never be more than one record returned.
    """
    occurrence_id = request.args.get(
        OCCURRENCE_ID_QUERY_PARAMETER, type=str, default=None
    )
    provider = ','.join(request.args.getlist(PROVIDER_QUERY_PARAMETER))
    if len(provider) == 0:
        provider = None
    resolver_service = controller.ResolveSvc()
    return resolver_service.GET(occid=occurrence_id, provider=provider)
