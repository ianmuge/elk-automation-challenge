

from ..kibana_basepage import KibanaBasePage, data_test_subj
from webium import Find, Finds
from selenium.webdriver.common.by import By
from webium.wait import wait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import locale


class DiscoverPage(KibanaBasePage):
    '''
    Kibana Discover Page
    '''

    query_hits_label = Find(**data_test_subj('discoverQueryHits'))
    new_button = Find(**data_test_subj('discoverNewButton'))
    save_button = Find(**data_test_subj('discoverSaveButton'))
    open_button = Find(**data_test_subj('discoverOpenButton'))
    share_button = Find(**data_test_subj('discoverShareButton'))
    time_picker_button = Find(**data_test_subj('globalTimepickerButton'))

    sidebar_item_fields = Finds(by=By.CLASS_NAME, value='sidebar-item')

    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        super().__init__(**kwargs)
        self.url += '/app/kibana#/discover'

    def loaded(self):
        wait(lambda: self.is_element_present('query_hits_label'), waiting_for='query_hits_label to be visible')

    def click_pattern(self, pattern):
        sidebar = IndexPatternSideList()
        sidebar.click_pattern(pattern)

    def get_query_hits(self):
        hits = self.query_hits_label.text
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        return locale.atoi(hits)

    def get_available_fields(self):
        fields = []
        for elem in self.sidebar_item_fields:
            fields.append(elem.text)
        return fields

    def get_hits(self, pattern):
        self.open()
        self.wait_for_loading_indicator()
        self.click_pattern(pattern)
        self.wait_for_loading_indicator()
        try:
            wait(lambda: int(self.get_query_hits()) > 0, timeout_seconds=7)
        except:
            pass
        return int(self.get_query_hits())


class IndexPatternOptions(WebElement):
    patterns = Finds(by=By.CSS_SELECTOR, value='div[role="option"]')


class IndexPatternSideList(KibanaBasePage):

    index_pattern_link = Find(by=By.CLASS_NAME, value='index-pattern')
    index_pattern_dropdown = Find(by=By.CLASS_NAME, value='index-pattern-selection')
    index_pattern_dropdown_options = Find(IndexPatternOptions, by=By.CLASS_NAME, value='index-pattern-selection')
    index_pattern_field = Find(by=By.CLASS_NAME, value='ui-select-search')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        wait(lambda: self.is_element_present('index_pattern_link') or
             self.is_element_present('index_pattern_dropdown'),
             waiting_for='Wait for index pattern')

    def click_pattern(self, pattern):
        if self.is_element_present('index_pattern_link'):
            if self.index_pattern_link.text == pattern:
                return
        elif self.is_element_present('index_pattern_dropdown'):
            self.index_pattern_dropdown.click()
            for elem in self.index_pattern_dropdown_options.patterns:
                if elem.text == pattern:
                    try:
                        elem.click()
                    except:
                        if self.is_element_present('index_pattern_field'):
                            self.index_pattern_field.clear()
                            self.index_pattern_field.send_keys(pattern)
                            self.index_pattern_field.send_keys(Keys.RETURN)
                        else:
                            raise NoSuchElementException('Unable to click: ' + pattern)
                    return
        raise NoSuchElementException('Index pattern not found: ' + pattern)
