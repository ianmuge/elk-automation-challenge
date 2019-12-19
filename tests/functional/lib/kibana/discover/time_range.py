
from ..kibana_basepage import KibanaBasePage, data_test_subj
from webium import Find, Finds
from selenium.webdriver.common.by import By
from webium.wait import wait
from webium.controls.select import Select
from selenium.webdriver.remote.webelement import WebElement
from collections import namedtuple


class TimeRangeQuick(KibanaBasePage):
    '''
    Kibana Discover Page: Time Range Screen
    '''

    _options = namedtuple('_options', ['today', 'this_week', 'this_month', 'this_year', 'the_day_so_far', 'week_to_date', 'month_to_date', 'year_to_date',
                                       'yesterday', 'day_before_yesterday', 'this_day_last_week', 'previous_week', 'previous_month', 'previous_year',
                                       'last_fifteen_minutes', 'last_thirty_minutes', 'last_hour', 'last_four_hours', 'last_twelve_hours', 'last_twenty_four_hours', 'last_seven_days',
                                       'last_thirty_days', 'last_sixty_days', 'last_ninety_days', 'last_six_months', 'last_year', 'last_two_years', 'last_five_years'])
    link_options = _options('Today', 'This week', 'This month', 'This year', 'The day so far', 'Week to date', 'Month to date', 'Year to date',
                            'Yesterday', 'Day before yesterday', 'This day last week', 'Previous week', 'Previous month', 'Previous year',
                            'Last 15 minutes', 'Last 30 minutes', 'Last 1 hour', 'Last 4 hours', 'Last 12 hours', 'Last 24 hours', 'Last 7 days',
                            'Last 30 days', 'Last 60 days', 'Last 90 days', 'Last 6 months', 'Last 1 year', 'Last 2 years', 'Last 5 years')

    quick_link = ''
    relative_link = ''
    absolute_link = ''

    time_picker_button = Find(**data_test_subj('globalTimepickerButton'))
    advanced_options_link = Find(by=By.LINK_TEXT, value='advanced options')
    index_pattern_id_field = Find(**data_test_subj('createIndexPatternIdInput'))

    time_filter_dropdown = Find(Select, **data_test_subj('createIndexPatternTimeFieldSelect'))
    refresh_fields_link = Find(by=By.LINK_TEXT, value='refresh fields')

    create_button = Find(**data_test_subj('createIndexPatternCreateButton'))

    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        super().__init__(**kwargs)
        self.url += '/app/kibana#/discover'


class TimeRangeQuickLink(WebElement):

    def update(self):
        ind = TimeRangeQuick.index(self.text)
        attr = TimeRangeQuick._options._fields[ind]
        setattr(self, attr, self)


class TimeRangeQuickList(KibanaBasePage):

    time_range_quick_list = Finds(TimeRangeQuickLink, by=By.CSS_SELECTOR, value='div.kbn-timepicker-section > ul > li > a')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        wait(lambda: len(self.time_range_quick_list) > 0, waiting_for='Time ranges in quick list')
