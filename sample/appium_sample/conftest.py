import pytest
from appium import webdriver


@pytest.fixture(autouse=True)
def app():
    global app_driver
    # APP定义运行环境
    desired_caps = {
        'deviceName': 'YAL_AL10',
        'automationName': 'appium',
        'platformName': 'Android',
        'platformVersion': '10.0',
        'appPackage': 'com.android.calculator2',
        'appActivity': '.Calculator',
    }
    app_driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return app_driver


@pytest.fixture(autouse=True)
def app_close():
    yield app_driver
    app_driver.quit()
