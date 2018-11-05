try:
    from unittest import mock
except ImportError:
    import mock
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.common.exceptions import NoSuchElementException

from page_objects import PageObject, PageElement, PageElements


@pytest.fixture()
def webdriver():
    return mock.Mock(spec=WebDriver)


class TestConstructor:

    def test_page_element(self):
        elem_id = PageElement(id_='id')
        elem_name = PageElement(name='name')
        elem_class = PageElement(class_='class')
        elem_tag = PageElement(tag='input')
        elem_link_text = PageElement(link_text='this_is_link')
        elem_partial_link_text = PageElement(partial_link_text='is_link')
        elem_xpath = PageElement(xpath='//*[@id="kk"]')
        elem_css = PageElement(css='#id')
        assert elem_id.locator == (By.ID, 'id')
        assert elem_name.locator == (By.NAME, 'name')
        assert elem_class.locator == (By.CLASS_NAME, 'class')
        assert elem_tag.locator == (By.TAG_NAME, 'input')
        assert elem_link_text.locator == (By.LINK_TEXT, 'this_is_link')
        assert elem_partial_link_text.locator == (By.PARTIAL_LINK_TEXT, 'is_link')
        assert elem_xpath.locator == (By.XPATH, '//*[@id="kk"]')
        assert elem_css.locator == (By.CSS_SELECTOR, '#id')

    def test_page_elements(self):
        elem = PageElements(id_='bar')
        assert elem.locator == (By.ID, 'bar')

    def test_page_element_bad_args(self):
        with pytest.raises(ValueError):
            PageElement()
        with pytest.raises(ValueError):
            PageElement(id_='foo', xpath='bar')


class TestGet:

    def test_get_element_with_context(self, webdriver):
        class TestPage(PageObject):
            test_elem = PageElement(css='bar', context=True)

        page = TestPage(webdriver)
        elem = mock.Mock(spec=WebElement, name="My Elem")
        res = page.test_elem(elem)
        assert elem.find_element.called_once_with(By.CSS_SELECTOR, 'bar')
        assert res == elem.find_element.return_value

    def test_get_not_found(self, webdriver):
        class TestPage(PageObject):
            test_elem = PageElement(id_='bar')

        page = TestPage(webdriver)
        webdriver.find_element.side_effect = NoSuchElementException
        assert page.test_elem is None

    def test_get_unattached(self):
        assert PageElement(css='bar').__get__(None, None) is None

    def test_get_multi(self, webdriver):
        class TestPage(PageObject):
            test_elems = PageElements(css='foo')

        webdriver.find_elements.return_value = ["XXX", "YYY"]
        page = TestPage(webdriver)
        assert page.test_elems == ["XXX", "YYY"]
        assert webdriver.find_elements.called_once_with(By.CSS_SELECTOR, 'foo')

    def test_get_multi_not_found(self, webdriver):
        class TestPage(PageObject):
            test_elems = PageElements(css='foo')

        webdriver.find_elements.side_effect = NoSuchElementException
        page = TestPage(webdriver)
        assert page.test_elems == []


class TestSet:

    def test_set_descriptors(self, webdriver):
        class TestPage(PageObject):
            test_elem1 = PageElement(css='foo')

        page = TestPage(webdriver)
        elem = mock.Mock(spec=WebElement, name="My Elem")
        webdriver.find_element.return_value = elem
        page.test_elem1 = "XXX"
        assert webdriver.find_elements.called_once_with(By.CSS_SELECTOR, 'foo')
        elem.send_keys.assert_called_once_with('XXX')

    def test_cannot_set_with_context(self, webdriver):
        class TestPage(PageObject):
            test_elem = PageElement(css='foo', context=True)

        page = TestPage(webdriver)
        with pytest.raises(ValueError) as e:
            page.test_elem = 'xxx'
        assert "doesn't support elements with context" in e.value.args[0]

    def test_cannot_set_not_found(self, webdriver):
        class TestPage(PageObject):
            test_elem = PageElement(css='foo')

        page = TestPage(webdriver)
        webdriver.find_element.side_effect = NoSuchElementException

        with pytest.raises(ValueError) as e:
            page.test_elem = 'xxx'
        assert "element not found" in e.value.args[0]

    def test_set_multi(self, webdriver):
        class TestPage(PageObject):
            test_elems = PageElements(css='foo')

        page = TestPage(webdriver)
        elem1 = mock.Mock(spec=WebElement)
        elem2 = mock.Mock(spec=WebElement)
        webdriver.find_elements.return_value = [elem1, elem2]
        page.test_elems = "XXX"
        assert webdriver.find_elements.called_once_with(By.CSS_SELECTOR, 'foo')
        elem1.send_keys.assert_called_once_with('XXX')
        elem2.send_keys.assert_called_once_with('XXX')

    def test_cannot_set_multi_with_context(self, webdriver):
        class TestPage(PageObject):
            test_elem = PageElements(css='foo', context=True)

        page = TestPage(webdriver)
        with pytest.raises(ValueError) as e:
            page.test_elem = 'xxx'
        assert "doesn't support elements with context" in e.value.args[0]

    def test_cannot_set_multi_not_found(self, webdriver):
        class TestPage(PageObject):
            test_elem = PageElements(css='foo')

        page = TestPage(webdriver)
        webdriver.find_elements.side_effect = NoSuchElementException

        with pytest.raises(ValueError) as e:
            page.test_elem = 'xxx'
        assert "no elements found" in e.value.args[0]


class TestRootURI:

    def test_from_constructor(self, webdriver):
        class TestPage(PageObject):
            pass

        page = TestPage(webdriver, url="http://example.com")
        assert page.root_uri == 'http://example.com'

    def test_from_webdriver(self):
        class TestPage(PageObject):
            pass
        webdriver = mock.Mock(spec=WebDriver, url="http://example.com/foo")
        page = TestPage(webdriver)
        assert page.root_uri == 'http://example.com/foo'

    def test_get(self, webdriver):
        class TestPage(PageObject):
            pass
        page = TestPage(webdriver, url="http://example.com")
        page.get('/foo/bar')
        assert webdriver.get.called_once_with("http://example.com/foo/bar")

    def test_get_no_root(self, webdriver):
        class TestPage(PageObject):
            pass
        page = TestPage(webdriver)
        page.get('/foo/bar')
        assert webdriver.get.called_once_with("/foo/bar")


class TestTimeOut:

    def test_setting_time_out(self):
        elem = PageElement(css='foo', time_out=10)
        assert elem.locator == (By.CSS_SELECTOR, 'foo')


class TestDescribe:

    def test_setting_describe(self):
        elem = PageElement(name='wd', describe="this is search input")
        assert elem.locator == (By.NAME, 'wd')


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_page_objects.py"])
