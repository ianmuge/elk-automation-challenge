from google.oauth2 import service_account
from google.cloud.container import ClusterManagerClient
from kubernetes import client, config
import os
import unittest
import config as cfg

class TestPods(unittest.TestCase):
    def setUp(self):
        self.project_id = cfg.project_id
        self.zone = cfg.zone
        self.cluster_id = cfg.cluster_id
        self.namespace = cfg.namespace
        SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
        credentials = service_account.Credentials.from_service_account_file('./service-account.json', scopes=SCOPES)
        cluster_manager_client = ClusterManagerClient(credentials=credentials)
        cluster = cluster_manager_client.get_cluster(self.project_id, self.zone, self.cluster_id)
        configuration = client.Configuration()
        configuration.host = "https://" + cluster.endpoint + ":443"
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + credentials.token}
        self.configuration=configuration

    def test_pods(self):
        client.Configuration.set_default(self.configuration)
        v1 =client.CoreV1Api()
        pods=v1.list_namespaced_pod(self.namespace)
        self.assertGreaterEqual(len(pods.items),11)




