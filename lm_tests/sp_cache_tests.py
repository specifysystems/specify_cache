"""lm_test style tests for the Specify cache."""
import requests

import lmtest.base.test_base as test_base


# .....................................................................................
class SpCacheCollectionTest(test_base.LmTest):
    """Collection tests (create, get, delete)."""

    # .............................
    def __init__(self, collection_values_json, collection_endpoint):
        """Constructor for collection test.

        Args:
            collection_values_json (dict): A dictionary of collection values.
            collection_endpoint (str): The API endpoint for collections.
        """
        test_base.LmTest.__init__(self)
        self.collection_endpoint = collection_endpoint
        self.collection_config = collection_values_json
        self.test_name = 'Specify Cache Collection Test for {}'.format(
            self.collection_config['collection_id']
        )

    # .............................
    def __repr__(self):
        """Return a string representation of this test."""
        return self.test_name

    # .............................
    def run_test(self):
        """Run the test."""
        collection_id = self.collection_config['collection_id']
        # Make sure that the collection doesn't exist
        try:
            requests.get('{}/{}'.format(self.collection_endpoint, collection_id))
            raise ValueError(
                'Found collection: {} when it should not exist (1)'.format(
                    collection_id
                )
            )
        except requests.NotFound:
            pass

        # POST the collection
        requests.post(self.collection_endpoint, json=self.collection_config)

        # GET the collection
        collection_get_response = requests.get(
            '{}/{}'.format(self.collection_endpoint, collection_id)
        )

        # DELETE the collection
        requests.delete('{}/{}'.format(self.collection_endpoint, collection_id))

        # Make sure that the collection is gone again
        try:
            requests.get('{}/{}'.format(self.collection_endpoint, collection_id))
            raise ValueError(
                'Found collection: {} when it should not exist (2)'.format(
                    collection_id
                )
            )
        except requests.NotFound:
            pass


# .....................................................................................
class SpCacheCollectionOccurrencePostTest(test_base.LmTest):
    """Test posting data for a collection."""

    # .............................
    def __init__(self, dwca_filename, occurrence_endpoint):
        """Constructor for occurrences post test.

        Args:
            dwca_filename (str): File location of DarwinCore Archive to POST.
            occurrence_endpoint (str): URL for posting occurrences.
        """
        test_base.LmTest.__init__(self)
        self.dwca_filename = dwca_filename
        self.occurrence_endpoint = occurrence_endpoint
        self.test_name = 'Specify Cache Collection Occurrence Test for {}'.format(
            self.occurrence_endpoint
        )

    # .............................
    def __repr__(self):
        """Return a string representation of this test."""
        return self.test_name

    # .............................
    def run_test(self):
        """Run the test."""
        with open(self.dwca_filename, mode='rb') as dwca_file:
            data = dwca_file.read()
        resp = requests.post(self.occurrence_endpoint, data=data)
        if resp.status_code != 204:
            raise test_base.LmTestFailure(
                'Occurrence data post at {} responded with code {}'.format(
                    self.occurrence_endpoint, resp.status_code
                )
            )
