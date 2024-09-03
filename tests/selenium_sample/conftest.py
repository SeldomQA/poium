import pytest
from selenium import webdriver


@pytest.fixture(scope='session', autouse=True)
def browser():
    global driver
    options = webdriver.ChromeOptions()
    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    return driver


@pytest.fixture(scope="session", autouse=True)
def browser_close():
    yield driver
    driver.quit()
