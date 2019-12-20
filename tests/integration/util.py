import requests
import json
import os
import config as cfg
def send_data(url,method="GET",data=None,headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application / json"
        }
    response = requests.request(method, url, headers=headers, data=data)
    return response
def create_test_index(url,index):
    try:
        url = "{0}{1}".format(url, index)
        response = send_data(url, "PUT")
    except:
        pass

def remove_test_index(url,index):
    try:
        url = "{0}{1}".format(url, index)
        response = send_data(url, "DELETE")
    except:
        pass
def sample_data(url,index):
    try:
        data = {"name": "Jane Doe"}
        payload = json.dumps(data)
        url = "{0}{1}{2}".format(url, index, "/doc/1")
        response = send_data(url, "POST", data=payload)
    except:
        pass

def bulk_sample_data(base_url,index):
    try:
        file = cfg.es_sample_data_path
        # if file and not os.path.isfile(file):
        #     raise FileNotFoundError('File not found: ' + file)
        url = "{0}{1}{2}".format(base_url, index, "/_bulk")
        file = open(file, 'rb')
        data = file.read()
        file.close()
        response = send_data(url, "POST", data=data)
        return response
    except Exception as exc:
        print("{0}".format(exc))

