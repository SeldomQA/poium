import pytest
from selenium import webdriver


@pytest.fixture(scope='session', autouse=True)
def browser():
    global driver
    driver = webdriver.Chrome()
    return driver


@pytest.fixture(scope="session", autouse=True)
def browser_close():
    yield driver
    driver.quit()
