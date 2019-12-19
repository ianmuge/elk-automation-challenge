import unittest
import util
import requests
import config as cfg


class TestCluster(unittest.TestCase):
    def setUp(self):
        self.endpoint="{0}://{1}:{2}/".format(cfg.es_protocol,cfg.es_host,cfg.es_port)
    def test_endpoint_health(self):
        response=util.send_data(self.endpoint)
        self.assertEqual(response.status_code, 200)
    def test_cluster_running(self):
        response = util.send_data(self.endpoint)
        json_data = response.json()
        self.assertNotEqual(json_data["cluster_uuid"], "_na_")
        self.assertEqual(json_data["cluster_name"], "k8s-logs")
    def test_cluster_health(self):
        url="{0}{1}".format(self.endpoint,"_cluster/health?pretty")
        response = util.send_data(url)
        json_data = response.json()
        self.assertEqual(json_data["status"], "green")
        self.assertEqual(json_data["timed_out"], False)
        self.assertGreater(json_data["number_of_nodes"], 1)

    # def test_generic(self):
    #     headers = {
    #         'Content-Type': 'application/json'
    #     }
    #     response = requests.request("GET", self.endpoint, headers=headers)
    #     response.json()
if __name__ == "__main__":
    unittest.main()

