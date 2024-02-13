import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

global app_driver

@pytest.fixture(autouse=True)
def app():
    global app_driver
    # APP定义运行环境
    capabilities = {
        "automationName": "UiAutomator2",
        "platformName": "Android",
        "appPackage": "com.meizu.flyme.flymebbs",
        "appActivity": "com.meizu.myplus.ui.splash.SplashActivity",
        "noReset": True,
    }
    options = UiAutomator2Options().load_capabilities(capabilities)
    app_driver = webdriver.Remote('http://localhost:4723', options=options)
    return app_driver


@pytest.fixture(autouse=True)
def app_close():
    yield app_driver
    app_driver.quit()
