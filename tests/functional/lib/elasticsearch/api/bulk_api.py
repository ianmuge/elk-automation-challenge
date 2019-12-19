

import os.path
from lib.api_session import ApiSession


class ElasticsearchBulkApi:
    '''
    Elasticsearch bulk api
    '''

    def __init__(self, api_session: ApiSession, **kwargs):
        '''
        Constructor
        '''
        self.api = api_session
        self.api.update_headers({'Content-Type': 'application/x-ndjson'})

    def post(self, data=None, file=None, index=None, doc_type=None, refresh_wait=True, **kwargs):
        if not data and not file:
            raise IOError('data or file must be specified')
        if file and not os.path.isfile(file):
            raise FileNotFoundError('File not found: ' + file)
        if index and doc_type:
            path = ('/%s/%s/_bulk' % (index, doc_type))
        elif index:
            path = ('/%s/_bulk' % (index))
        else:
            path = '/_bulk'

        if refresh_wait:
            path += '?refresh=wait_for'

        if file:
            data = open(file, 'rb').read()

        response = self.api.post(path, data=data)

        return response
