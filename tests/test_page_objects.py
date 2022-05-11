try:
    from unittest import mock
except ImportError:
    import mock
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.common.exceptions import NoSuchElementException

from poium import Page, Element, Elements

@pytest.fixture()
def webdriver():
    return mock.Mock(spec=WebDriver)


class TestConstructor:

    def test_page_element(self):
        elem_id = Element(id_='id')
        elem_name = Element(name='name')
        elem_class = Element(class_name='class')
        elem_tag = Element(tag='input')
        elem_link_text = Element(link_text='this_is_link')
        elem_partial_link_text = Element(partial_link_text='is_link')
        elem_xpath = Element(xpath='//*[@id="kk"]')
        elem_css = Element(css='#id')
        assert elem_id.k == 'id_'
        assert elem_name.k == "name"
        assert elem_class.k == "class_name"
        assert elem_tag.k == "tag"
        assert elem_link_text.k == "link_text"
        assert elem_partial_link_text.k == "partial_link_text"
        assert elem_xpath.k == "xpath"
        assert elem_css.k == "css"

    def test_page_element_bad_args(self):
        with pytest.raises(ValueError):
            Element()
        with pytest.raises(ValueError):
            Element(id_='foo', xpath='bar')


class TestGet:

    def test_get_unattached(self):
        assert Element(css='bar').__get__(None, None) is None


class TestSet:

    def test_set_multi(self, webdriver):
        class TestPage(Page):
            test_elems = Elements(css='foo')

        page = TestPage(webdriver)
        elem1 = mock.Mock(spec=WebElement)
        elem2 = mock.Mock(spec=WebElement)
        webdriver.find_elements.return_value = [elem1, elem2]
        page.test_elems = "XXX"
        assert webdriver.find_elements.called_once_with(By.CSS_SELECTOR, 'foo')
        elem1.send_keys.assert_called_once_with('XXX')
        elem2.send_keys.assert_called_once_with('XXX')


class TestRootURI:

    def test_from_constructor(self, webdriver):
        class TestPage(Page):
            pass

        page = TestPage(webdriver, url="http://example.com")
        assert page.root_uri == 'http://example.com'

    def test_from_webdriver(self):
        class TestPage(Page):
            pass
        webdriver = mock.Mock(spec=WebDriver, url="http://example.com/foo")
        page = TestPage(webdriver)
        assert page.root_uri == 'http://example.com/foo'

    def test_get(self, webdriver):
        class TestPage(Page):
            pass
        page = TestPage(webdriver, url="http://example.com")
        page.get('/foo/bar')
        assert webdriver.get.called_once_with("http://example.com/foo/bar")

    def test_get_no_root(self, webdriver):
        class TestPage(Page):
            pass
        page = TestPage(webdriver)
        page.get('/foo/bar')
        assert webdriver.get.called_once_with("/foo/bar")


class TestTimeOut:

    def test_setting_time_out(self):
        elem = Element(css='foo', timeout=10)
        assert elem.k == "css"


class TestDescribe:

    def test_setting_describe(self):
        elem = Element(name='wd', describe="this is search input")
        assert elem.k == "name"


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_page_objects.py"])
