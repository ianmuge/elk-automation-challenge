import unittest
import util
import requests
import config as cfg

class TestIndex(unittest.TestCase):
    def setUp(self):
        self.endpoint="{0}://{1}:{2}/".format(cfg.es_protocol,cfg.es_host,cfg.es_port)
        self.index=cfg.es_test_index

    def tearDown(self):
        util.remove_test_index(self.endpoint,self.index)
    def test_index_create(self):
        url="{0}{1}".format(self.endpoint,self.index)
        response=util.send_data(url,"PUT")
        self.assertIn(response.status_code, [200,201])

    def test_index_exists(self):
        util.create_test_index(self.endpoint, self.index)
        url = "{0}{1}".format(self.endpoint, self.index)
        response = util.send_data(url)
        self.assertEqual(response.status_code, 200)
        assert "error" not in response.text
        url = "{0}{1}".format(self.endpoint, "_cat/indices?v=")
        response = util.send_data(url)
        assert "bank" in response.text

if __name__ == "__main__":
    unittest.main()

