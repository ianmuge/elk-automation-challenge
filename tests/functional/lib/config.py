

import os
from munch import Munch
from webium import settings
from selenium.webdriver import Chrome, Firefox, Safari, Ie, Edge, PhantomJS


def build_url(d1, d2):
    valid_keys = ['protocol', 'host', 'port']
    key_exists = []
    for key in valid_keys:
        key_exists.append(key in d1.keys())
    if not all(key_exists):
        raise AttributeError('Valid keys: %s not found in %s' %
                             (valid_keys, str(d1.keys())))
    if d2.xpack:
        d1.protocol = 'https'
    url = '%s://%s:%s' % (d1.protocol, d1.host, str(d1.port))
    return url


def check_browser(browser):
    valid_browsers = [Chrome, Firefox, Safari, Ie, Edge, PhantomJS]
    if browser not in valid_browsers:
        raise AttributeError('Invalid browser: %s' % (browser))
    return browser


testing = Munch()
browser = Munch()
elasticsearch = Munch()
kibana = Munch()

testing.xpack = os.getenv('AIT_XPACK', False)

elasticsearch.protocol = os.getenv('AIT_ELASTICSEARCH_PROTOCOL', 'http')
elasticsearch.host = os.getenv('AIT_ELASTICSEARCH_HOST', '34.77.139.253')
elasticsearch.port = os.getenv('AIT_ELASTICSEARCH_PORT', 9200)
elasticsearch.username = os.getenv('AIT_ELASTICSEARCH_USERNAME', '')
elasticsearch.password = os.getenv('AIT_ELASTICSEARCH_PASSWORD', '')
elasticsearch.xpack = testing.xpack
elasticsearch.url = os.getenv('AIT_ELASTICSEARCH_URL', build_url(elasticsearch, testing))
print(elasticsearch)

kibana.protocol = os.getenv('AIT_KIBANA_PROTOCOL', 'http')
kibana.host = os.getenv('AIT_KIBANA_HOST', '35.233.88.232')
kibana.port = os.getenv('AIT_KIBANA_PORT', 5601)
kibana.username = os.getenv('AIT_KIBANA_USERNAME', '')
kibana.password = os.getenv('AIT_KIBANA_PASSWORD', '')
kibana.xpack = testing.xpack
kibana.url = os.getenv('AIT_KIBANA_URL', build_url(kibana, testing))
print(kibana)

browser.type = os.getenv('AIT_BROWSER', Chrome)
browser.headless = os.getenv('AIT_RUN_HEADLESS_BROWSER', False)
settings.driver_class = check_browser(browser.type)
