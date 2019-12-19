

from selenium.webdriver.common.by import By
from webium import BasePage, Find
from webium.wait import wait
from .. import config

def data_test_subj(elem_names):
    if not elem_names:
        raise IOError('Element name/s can not be empty')
    return {'by': By.CSS_SELECTOR,
            'value': " ".join(['[data-test-subj={}]'.format(name) for name in elem_names.split()])}

class KibanaBasePage(BasePage):

    loading_indicator = Find(**data_test_subj('globalLoadingIndicator'))

    def __init__(self, url=config.kibana.url, **kwargs):
        self.url = url.strip('/')
        super().__init__(**kwargs)

    def wait_for_loading_indicator(self, timeout=5):
        try:
            wait(lambda: self.is_element_present('loading_indicator') is True,
                 waiting_for='Loading indicator is displayed', timeout_seconds=timeout)
        except:
            pass
        wait(lambda: self.is_element_present('loading_indicator') is False,
             waiting_for='Loading indicator is not displayed', timeout_seconds=timeout)
