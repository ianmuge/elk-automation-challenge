

import pytest
from data import info
from lib.elasticsearch.api.bulk_api import ElasticsearchBulkApi
from lib.kibana.discover.discover_page import DiscoverPage
from lib.kibana.management.index_patterns_page import IndexPatternsPage


@pytest.mark.usefixtures('kibana_login_as_elastic_user')
class TestBasicIntegration:

    testdata = [pytest.mark.filebeat('filebeat-*'),
                pytest.mark.packetbeat('packetbeat-*'),
                pytest.mark.metricbeat('metricbeat-*'),
                pytest.mark.logstash('logstash-*')]

    @pytest.mark.kibana
    def test_discover_page_hits_equals_num_entries(self, es_api_session):
        """Verify number of hits is equal to number of entries in bank.json posted in kibana discover page"""
        data = info.es_bank_accounts
        kibana_index = data.index + '*'
        esapi = ElasticsearchBulkApi(es_api_session)
        response = esapi.post(file=data.file,
                              index=data.index,
                              doc_type=data.type)
        index_patterns_page = IndexPatternsPage()
        index_patterns_page.create_index(kibana_index, IndexPatternsPage.TIME_FILTER_NOT_APPLICABLE)
        discover_page = DiscoverPage()
        hits = discover_page.get_hits(kibana_index)
        assert hits == data.entries

    @pytest.mark.kibana
    @pytest.mark.parametrize("kibana_index", testdata)
    def test_discover_page_hits_greater_than_zero(self, kibana_index):
       """Verify number of hits is great than zero in kibana discover page"""
       index_patterns_page = IndexPatternsPage()
       index_patterns_page.create_index(kibana_index, IndexPatternsPage.TIME_FILTER_TIMESTAMP)
       discover_page = DiscoverPage()
       hits = discover_page.get_hits(kibana_index)
       assert hits > 0
