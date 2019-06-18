import pytest
import os
import requests
import json
import re

from appium import webdriver
import testobject

def update_job(session_id, result):
    result_json = json.dumps({"passed": result})
    requests.put(
        'https://app.testobject.com/api/rest/v2/appium/session/' + session_id + '/test/',
        headers = { 'Content-Type': 'application/json',},  
        data = '{"passed": true}' 
    )
    #endpoint = 'https://app.testobject.com/api/rest/appium/v2/session/{}/test/'.format(session_id)
    #requests.put(endpoint, data=result_json)

@pytest.yield_fixture(scope='function')
def driver(request):
    
    SAUCE_USERNAME = os.environ['SAUCE_USERNAME']
    SAUCE_ACCESS_KEY = os.environ['SAUCE_ACCESS_KEY']

    caps = {
        'appiumVersion':    '1.9.1',
        'browserName':      '',
        'platformName':     'iOS',
        'platformVersion':  '12.1.4',
        'deviceOrientation':'portrait',
        'phoneOnly': False,
        'tabletOnly': False,
        'privateDevicesOnly': False 
    }

    rdc_key = os.environ['TESTOBJECT_API_KEY']
    rdc_user = os.environ['TESTOBJECT_USERNAME']
    caps['testobject_api_key'] = rdc_key

    rdc_api = testobject.TestObject(rdc_user, rdc_key) 

    sauce_url = "http://us1.appium.testobject.com/wd/hub"

    browser = webdriver.Remote(sauce_url, desired_capabilities=caps)
    
    yield browser

    rdc_api.watcher.report_test_result(browser.session_id, True)
    
    browser.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for Sauce Labs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
    return rep
