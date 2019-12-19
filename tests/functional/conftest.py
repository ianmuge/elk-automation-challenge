

import pytest
from webium.driver import close_driver
from .lib.api_session import ApiSession
from .lib import config
from webium.wait import wait
from .lib.kibana.login.login_page import LoginPage
from .lib.kibana.sidebar.sidebar import Sidebar
from xvfbwrapper import Xvfb
import time

@pytest.fixture(scope='session', autouse=False)
def xvfb_launcher(request):
    if config.browser.headless:
        vdisplay = Xvfb()
        vdisplay.start()
        return vdisplay

@pytest.fixture(scope='session', autouse=False)
def es_api_session(request):
    api = ApiSession(cfg=config.elasticsearch)
    return api

@pytest.fixture(scope='session', autouse=False)
def kibana_login_as_elastic_user(request):
    if config.testing.xpack:
        login_page = LoginPage()
        login_page.login(config.elasticsearch.username, config.elasticsearch.password)
        sidebar = Sidebar()
        sidebar.loaded()
        wait(lambda: sidebar.is_link_visible(config.elasticsearch.username) is True)

@pytest.fixture(scope='session', autouse=True)
def teardown(request, xvfb_launcher):
    @request.addfinalizer
    def tear_down():
        close_driver()
        if config.browser.headless:
            xvfb_launcher.stop()
