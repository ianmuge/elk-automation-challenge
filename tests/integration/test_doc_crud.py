import unittest
import util
import requests
import config as cfg
import json
import os

class TestDocCrud(unittest.TestCase):
    def setUp(self):
        self.endpoint="{0}://{1}:{2}/".format(cfg.es_protocol,cfg.es_host,cfg.es_port)
        self.index=cfg.es_test_index
        util.create_test_index(self.endpoint, self.index)
    def tearDown(self):
        util.remove_test_index(self.endpoint,self.index)
    def test_create(self):
        data= {"name": "Jane Smith"}
        payload=json.dumps(data)
        url="{0}{1}{2}".format(self.endpoint,self.index,"/doc")
        response = util.send_data(url, "POST",data=payload)
        json_data = response.json()
        self.assertIn(response.status_code, [200,201])
        self.assertEqual(json_data["result"],"created")
    def test_read(self):
        util.sample_data(self.endpoint, self.index)
        url = "{0}{1}{2}".format(self.endpoint, self.index, "/doc/1")
        response = util.send_data(url, "GET")
        json_data = response.json()
        self.assertEqual(json_data["found"], True)
        self.assertEqual(json_data["_id"], "1")
    def test_update(self):
        util.sample_data(self.endpoint, self.index)
        data = {"name": "Jane Smith"}
        payload = json.dumps(data)
        url = "{0}{1}{2}".format(self.endpoint, self.index, "/doc/1")
        response = util.send_data(url, "PUT",data=payload)
        json_data = response.json()
        self.assertEqual(json_data["result"], "updated")
        self.assertEqual(json_data["_id"], "1")
        self.assertGreater(json_data["_version"], 1)

    def test_delete(self):
        util.sample_data(self.endpoint, self.index)
        url = "{0}{1}{2}".format(self.endpoint, self.index, "/doc/1")
        response = util.send_data(url, "DELETE")
        json_data = response.json()
        self.assertEqual(json_data["result"], "deleted")
        self.assertEqual(json_data["_id"], "1")

        fetch_url = "{0}{1}{2}".format(self.endpoint, self.index, "/doc/1")
        fetch_response = util.send_data(fetch_url, "GET")
        fetch_json_data = fetch_response.json()
        self.assertEqual(fetch_json_data["found"], False)

    def test_bulk_api(self):
        file=cfg.es_sample_data_path
        # if file and not os.path.isfile(file):
        #     raise FileNotFoundError('File not found: ' + file)
        url = "{0}{1}{2}".format(self.endpoint, self.index, "/_bulk")
        file=open(file, 'rb')
        data = file.read()
        file.close()
        response = util.send_data(url, "POST", data=data)
        json_data = response.json()
        self.assertEqual(json_data["errors"], False)

    def test_search(self):
        util.bulk_sample_data(self.endpoint, self.index)
        util.bulk_sample_data(self.endpoint, self.index)
        # print(res.json())
        data={
            "query": {
                "match_all": {}
            },
            "sort": [
                {
                    "balance": {
                        "order": "desc"
                    }
                }
            ]
        }
        payload = json.dumps(data)
        url = "{0}{1}{2}".format(self.endpoint, self.index, "/_search")
        response = util.send_data(url, "POST", data=payload)
        json_data = response.json()
        # print(json_data["hits"]['total']['value'])
        self.assertEqual(json_data["timed_out"], False)
        self.assertGreaterEqual(json_data["hits"]['total']['value'], 0)

if __name__ == "__main__":
    unittest.main()

