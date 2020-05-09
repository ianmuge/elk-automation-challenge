from google.oauth2 import service_account
from google.cloud.container import ClusterManagerClient
from kubernetes import client, config
import os
import unittest
import config as cfg


# class TestSetup(unittest.TestCase):
#     def setUp(self):
#         self.project_id = cfg.project_id
#         self.zone = cfg.zone
#         self.cluster_id = cfg.cluster_id
#         self.namespace = cfg.namespace
#
#
#

def test_gke():
    project_id = "interviews-dev"
    zone = "europe-west1-b"
    cluster_id = "interview-cluster"
    namespace = "monitoring"

    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
    credentials = service_account.Credentials.from_service_account_file('./service-account.json', scopes=SCOPES)
    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(cfg.project_id, cfg.zone, cfg.cluster_id)
    configuration = client.Configuration()
    configuration.host = "https://" + cluster.endpoint + ":443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)
    print(cluster)
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    pods = v1.list_pod_for_all_namespaces(watch=False)
    for i in pods.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


if __name__ == '__main__':
    test_gke()



