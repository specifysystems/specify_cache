"""Process a Darwin Core Archive and add the data to the Specify Cache."""
import argparse
import csv
import io
import xml.etree.ElementTree as ET
import zipfile

# import solr_controller as solr_app


DEFAULT_META_FILENAME = 'meta.xml'
DEFAULT_NAMESPACE = 'http://rs.tdwg.org/dwc/terms/'
TARGET_NAMESPACE = '{http://rs.tdwg.org/dwc/text/}'
CSV_PARAMS = [
    ('delimiter', 'fieldsTerminatedBy'),
    ('lineterminator', 'linesTerminatedBy'),
    ('quotechar', 'fieldsEnclosedBy'),
]
MY_PARAMS = [
    ('encoding', 'encoding'),
    ('num_header_rows', 'ignoreHeaderLines'),
    ('row_type', 'rowType'),
]
SOLR_POST_LIMIT = 1000


# .....................................................................................
def get_full_tag(tag, namespace=TARGET_NAMESPACE):
    """Get the full tag, including namespace, to search for.

    Args:
        tag (str): An XML tag without namespace.
        namespace (str): The namespace to prepend to the tag string.

    Returns:
        str - A full XML tag including namespace.
    """
    return '{}{}'.format(namespace, tag)


# .....................................................................................
def post_results(post_recs, collection_id):
    """Post results to Solr index and resolver.

    Args:
        post_recs (list of dict): A list of dictionaries representing records to post
            to solr.
        collection_id (str): An identifier associated with the collection containing
            these records.
    """
    # sp_solr = solr_app.get_specimen_solr()
    # sp_solr.add
    print('Post results to solr!')
    print('Create and post results to resolver!')
    year = 2021
    month = 5
    day = 4
    csv_lines = [
        'id,institutionCode,collectionCode,datasetName,basisOfRecord,year,month,day,url'
    ]
    for rec in post_recs:
        url = 'https://syftorium.org/sp_cache/collections/{}/specimens/{}'.format(
            collection_id, rec['id']
        )

        csv_lines.append(
            '{},{},{},{},{},{},{},{},{}'.format(
                rec['occurrenceID'],
                rec['institutionCode'],
                rec['collectionCode'],
                rec['datasetName'],
                rec['basisOfRecord'],
                year,
                month,
                day,
                url
            )
        )
    resolver_data = '\n'.join(csv_lines)
    print(resolver_data)


# .....................................................................................
def process_meta_xml(meta_contents):
    """Process the meta.xml file contents.

    Args:
        meta_contents (str): The string contents of a meta.xml file.

    Returns:
        (str, dict, dict, dict) - An occurrence filename, field dictionary, our
            parmeters dictionary, csv parameters dictionary.
    """
    # Convert bytes to string and process xml
    # Need to return occurrence filename and lookup
    occurrence_filename = None
    fields = {}
    # extensions = []
    constants = []
    root_el = ET.fromstring(meta_contents)
    core_el = root_el.find(get_full_tag('core'))
    # Process core
    my_params = {'encoding': 'utf8', 'num_header_rows': 0}
    csv_reader_params = {}
    for my_key, core_att in MY_PARAMS:
        if core_att in core_el.attrib.keys():
            my_params[my_key] = core_el.attrib[core_att]
    for csv_key, core_att in CSV_PARAMS:
        if core_att in core_el.attrib.keys():
            csv_reader_params[csv_key] = core_el.attrib[core_att]

    occurrence_filename = core_el.find(
        get_full_tag('files')
    ).find(get_full_tag('location')).text
    for field_el in core_el.findall(get_full_tag('field')):
        # Process field
        if 'index' in field_el.attrib.keys():
            fields[
                int(field_el.attrib['index'])
            ] = field_el.attrib['term'].split(DEFAULT_NAMESPACE)[1]
        else:
            constants.append((field_el.attrib['term'], field_el.attrib['default']))
    for id_el in core_el.findall(get_full_tag('id')):
        fields[int(id_el.attrib['index'])] = 'id'
    return occurrence_filename, fields, my_params, csv_reader_params


# .....................................................................................
def process_occurrence_file(
    occurrence_file,
    fields,
    my_params,
    csv_reader_params,
    collection_id
):
    """Process an occurrence file.

    Args:
        occurrence_file (file-like object): File-like object of occurrence data.
        fields (dict): A dictionary of fields in the occurrence file.
        my_params (dict): A dictionary of our parameters for processing data.
        csv_reader_params (dict): A dictionary of parameters to forward to csv.reader.
        collection_id (str): An identifier for the collection these data are from.
    """
    for _ in range(int(my_params['num_header_rows'])):
        print(next(occurrence_file))
    reader = csv.reader(occurrence_file, **csv_reader_params)
    solr_post_recs = []
    for row in reader:
        rec = {fields[idx]: row[idx] for idx in fields.keys()}
        solr_post_recs.append(rec)
        if len(solr_post_recs) >= SOLR_POST_LIMIT:
            post_results(solr_post_recs, collection_id)
            solr_post_recs = []
    if len(solr_post_recs) > 0:
        post_results(solr_post_recs, collection_id)


# .....................................................................................
def process_dwca(dwca_filename, collection_id, meta_filename=DEFAULT_META_FILENAME):
    """Process the Darwin Core Archive.

    Args:
        dwca_filename (str): A filename for a DarwinCore Archive file.
        collection_id (str): An identifier for the collection containing these data.
        meta_filename (str): A file contained in the archive containing metadata.
    """
    with zipfile.ZipFile(dwca_filename) as zip_archive:
        meta_xml_contents = zip_archive.read(meta_filename)
        occurrence_filename, fields, my_params, csv_reader_params = process_meta_xml(
            meta_xml_contents
        )
        process_occurrence_file(
            io.TextIOWrapper(
                zip_archive.open(
                    occurrence_filename, mode='r'
                )
            ), fields, my_params, csv_reader_params, collection_id
        )


# .....................................................................................
def main():
    """Main method for script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('collection_id', type=str, help='Collection identifier')
    parser.add_argument('dwca_filename', type=str, help='File path to DwC-A file')
    args = parser.parse_args()
    process_dwca(args.dwca_filename, args.collection_id)


# .....................................................................................
if __name__ == '__main__':
    main()
