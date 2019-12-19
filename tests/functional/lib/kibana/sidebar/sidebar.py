

import re
from ..kibana_basepage import KibanaBasePage, data_test_subj
from webium import Finds, Find
from webium.wait import wait
from webium.controls.link import Link
from webium.driver import get_driver
from ...ait_exceptions import IndexPatternDoesNotExist
from selenium.webdriver.common.by import By


class Sidebar(KibanaBasePage):
    '''
    Kibana Login Page
    '''

    DISCOVER = 'Discover'
    VISUALIZE = 'Visualize'
    DASHBOARD = 'Dashboard'
    TIMELION = 'Timelion'
    MACHINE_LEARNING = 'Machine Learning'
    GRAPH = 'Graph'
    DEV_TOOLS = 'Dev Tools'
    MONITORING = 'Monitoring'
    MANAGEMENT = 'Management'
    COLLAPSE = 'Collapse'
    EXPAND = 'Expand'
    LOGOUT = 'Logout'

    sidebar_main = Find(by=By.CLASS_NAME, value='global-nav__links')
    sidebar_links = Finds(Link, **data_test_subj('global-nav-link appLink'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def loaded(self):
        wait(lambda: self.is_element_present('sidebar_main') is True)

    def click_link_text(self, text):
        for link in self.sidebar_links:
            if link.text == text:
                link.click()
                break

    def is_link_visible(self, text):
        return text in self.sidebar_main.text.split('\n')
