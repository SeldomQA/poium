from page_objects import PageObject, PageElement, PageElements
from selenium.webdriver.common.by import By
import pytest


class TestConstructor:

    def test_page_element(self):
        elem = PageElement(css='foo')
        assert elem.locator == (By.CSS_SELECTOR, 'foo')

    def test_multi_page_element(self):
        elem = PageElements(id_='bar')
        assert elem.locator == (By.ID, 'bar')


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_page_objects.py"])
