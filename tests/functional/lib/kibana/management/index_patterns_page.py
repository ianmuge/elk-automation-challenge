

from ..kibana_basepage import KibanaBasePage, data_test_subj
from webium import Find
from selenium.webdriver.common.by import By
from webium.wait import wait
from webium.controls.select import Select
from webium.driver import get_driver
import re
from lib.ait_exceptions import IndexPatternDoesNotExist


class IndexPatternsPage(KibanaBasePage):
    '''
    Kibana Management Index Patterns Page
    '''

    TIME_FILTER_TIMESTAMP = '@timestamp'
    TIME_FILTER_DO_NOT_USE = 'I don\'t want to use the Time Filter'
    TIME_FILTER_NOT_APPLICABLE = True

    SUBMIT_BUTTON_TIME_FILTER_IS_REQUIRED = 'Time Filter field name is required'
    SUBMIT_BUTTON = 'Create'

    sidebar_list_elem = Find(by=By.CSS_SELECTOR, value='div.sidebar-list')

    index_pattern_field = Find(**data_test_subj('createIndexPatternNameInput'))
    advanced_options_link = Find(by=By.LINK_TEXT, value='advanced options')
    index_pattern_id_field = Find(**data_test_subj('createIndexPatternIdInput'))

    time_filter_dropdown = Find(Select, **data_test_subj('createIndexPatternTimeFieldSelect'))

    refresh_fields_link = Find(by=By.LINK_TEXT, value='refresh fields')

    submit_button = Find(by=By.CSS_SELECTOR, value='button[type="submit"]')

    set_default_index_button = Find(**data_test_subj('setDefaultIndexPatternButton'))

    # In 6.1.x
    next_button = Find(**data_test_subj('createIndexPatternGoToStep2Button'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url += '/app/kibana#/management/kibana/index'

    def loaded(self):
        wait(lambda: self.is_element_present('index_pattern_field') is True)

    def click_advanced_options(self):
        self.advanced_options_link.click()

    def click_submit_button(self):
        wait(lambda: self.submit_button.is_enabled())
        self.submit_button.click()

    def click_next_button(self):
        wait(lambda: self.next_button.is_enabled())
        self.next_button.click()

    def click_refresh_fields(self):
        self.refresh_fields_link.click()

    def click_set_as_default_index(self):
        self.set_default_index_button.click()

    def click_index_pattern(self, pattern):
        self.get_pattern_link_by_text(pattern).click()

    def pattern_in_sidebar(self, pattern):
        pattern_list_items = self.sidebar_list_elem.text.split('\n')
        if pattern in pattern_list_items:
            return True
        return False

    def get_pattern_link_by_text(self, pattern):
        return Find(by=By.LINK_TEXT, value=pattern, context=self)

    def enter_index_pattern(self, pattern):
        self.index_pattern_field.clear()
        if self.is_element_present('submit_button'):
            wait(lambda: not self.submit_button.is_enabled())
        if self.is_element_present('next_button'):
            wait(lambda: not self.next_button.is_enabled())
        self.index_pattern_field.send_keys(pattern)

    def check_pattern(self, pattern):
        if self.index_pattern_field.get_attribute('value') == pattern + '*':
            self.enter_index_pattern(pattern.rstrip('*'))

    def enter_index_pattern_id(self, pattern_id):
        if not self.is_element_present('index_pattern_id_field'):
            self.click_advanced_options()
        self.index_pattern_id_field.clear()
        self.index_pattern_id_field.send_keys(pattern_id)

    def get_index_id_from_url(self):
        current_url = get_driver().current_url
        regex = re.compile('/indices/(.+)\?')
        match = regex.search(current_url)
        if hasattr(match, 'groups'):
            return match.group(1)
        return None

    def select_time_filter(self, selfilter):
        wait(lambda: len(self.time_filter_dropdown.get_options()) > 1)
        self.time_filter_dropdown.select_by_visible_text(selfilter)

    def create_index(self, pattern_name, time_filter, pattern_id=None):
        self.open()
        self.loaded()
        if self.pattern_in_sidebar(pattern_name):
            self.click_index_pattern(pattern_name)
        else:
            self.enter_index_pattern(pattern_name)
            self.check_pattern(pattern_name)
            if self.is_element_present('next_button'):
                self.click_next_button()
            if pattern_id:
                self.enter_index_pattern_id(pattern_id)
            if time_filter != self.TIME_FILTER_NOT_APPLICABLE:
                self.select_time_filter(time_filter)
            self.click_submit_button()
        self.wait_for_loading_indicator()
        wait(lambda: self.get_index_id_from_url() is not None, timeout_seconds=5)
        index_id = self.get_index_id_from_url()
        if not index_id:
            raise IndexPatternDoesNotExist('Index pattern not created')
        return index_id
