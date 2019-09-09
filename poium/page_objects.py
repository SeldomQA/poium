import logging
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from appium.webdriver.common.mobileby import MobileBy

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Map PageElement constructor arguments to webdriver locator enums
LOCATOR_LIST = {
    # selenium
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME,
    # appium
    'ios_uiautomation': MobileBy.IOS_UIAUTOMATION,
    'ios_predicate': MobileBy.IOS_PREDICATE,
    'ios_class_chain': MobileBy.IOS_CLASS_CHAIN,
    'android_uiautomator': MobileBy.ANDROID_UIAUTOMATOR,
    'android_viewtag': MobileBy.ANDROID_VIEWTAG,
    'android_datamatcher': MobileBy.ANDROID_DATA_MATCHER,
    'accessibility_id': MobileBy.ACCESSIBILITY_ID,
    'image': MobileBy.IMAGE,
    'custom': MobileBy.CUSTOM,
}


class PageObject:
    """
    Page Object pattern.
    """

    def __init__(self, driver, url=None):
        """
        :param driver: `selenium.webdriver.WebDriver` Selenium webdriver instance
        :param url: `str`
        Root URI to base any calls to the ``PageObject.get`` method. If not defined
        in the constructor it will try and look it from the webdriver object.
        """
        self.driver = driver
        self.root_uri = url if url else getattr(self.driver, 'url', None)

    def get(self, uri):
        """
        :param uri:  URI to GET, based off of the root_uri attribute.
        """
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)
        self.driver.implicitly_wait(5)

    def run_script(self, js=None):
        """
        run JavaScript script
        """
        if js is None:
            raise ValueError("Please input js script")
        else:
            self.driver.execute_script(js)


class PageElement(object):
    """
    Page Element descriptor.
    :param css:    `str`
        Use this css locator
    :param id_:    `str`
        Use this element ID locator
    :param name:    `str`
        Use this element name locator
    :param xpath:    `str`
        Use this xpath locator
    :param link_text:    `str`
        Use this link text locator
    :param partial_link_text:    `str`
        Use this partial link text locator
    :param tag:    `str`
        Use this tag name locator
    :param class_:    `str`
        Use this class locator
    :param context: `bool`
        This element is expected to be called with context
    Page Elements are used to access elements on a page. The are constructed
    using this factory method to specify the locator for the element.
        >> from page import Page, PageElement
        >> class MyPage(Page):
                elem1 = PageElement(css='div.myclass')
                elem2 = PageElement(id_='foo')
                elem_with_context = PageElement(name='bar', context=True)
    Page Elements act as property descriptors for their Page Object, you can get
    and set them as normal attributes.
    """
    def __init__(self, context=False, timeout=5, describe=None, **kwargs):
        self.time_out = timeout
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        self.k, self.v = next(iter(kwargs.items()))
        try:
            self.locator = (LOCATOR_LIST[self.k], self.v)
        except KeyError:
            raise KeyError("Please use a locator：'id_'、'name'、'class_name'、'css'、'xpath'、'link_text'、'partial_link_text'.")
        self.has_context = bool(context)

    def get_element(self, context):
        try:
            elem = context.find_element(*self.locator)
        except NoSuchElementException:
            return None
        else:
            try:
                style_red = 'arguments[0].style.border="2px solid red"'
                context.execute_script(style_red, elem)
            except BaseException:
                return elem
            return elem

    def find(self, context):
        for i in range(1, self.time_out):
            logger.info("{n} times search, {elm} ".format(n=i, elm=self.locator))
            if self.get_element(context) is not None:
                return self.get_element(context)
        else:
            return self.get_element(context)

    def __get__(self, instance, owner, context=None):
        if not instance:
            return None

        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)

        if not context:
            context = instance.driver

        return self.find(context)

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elem = self.__get__(instance, instance.__class__)
        if not elem:
            raise ValueError("Can't set value, element not found")
        elem.send_keys(value)


class PageElements(PageElement):
    """
    Like `PageElement` but returns multiple results.
    >> from page import Page, PageElements
    >> class MyPage(Page):
            all_table_rows = PageElements(tag='tr')
            elem2 = PageElement(id_='foo')
            elem_with_context = PageElement(tag='tr', context=True)
    """
    def find(self, context):
        try:
            return context.find_elements(*self.locator)
        except NoSuchElementException:
            return []

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elems = self.__get__(instance, instance.__class__)
        if not elems:
            raise ValueError("Can't set value, no elements found")
        [elem.send_keys(value) for elem in elems]


class PageSelect(object):
    """
    Processing select drop-down selection box
    """
    def __init__(self, select_elem, value=None, text=None, index=None):
        if value is not None:
            Select(select_elem).select_by_value(value)
        elif text is not None:
            Select(select_elem).select_by_visible_text(text)
        elif index is not None:
            Select(select_elem).select_by_index(index)
        else:
            raise ValueError('"value" or "text" or "index" options can not be all empty.')


class PageWait(object):

    def __init__(self, elm, timeout=3):
        """
        wait webelement display
        """
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError("Type 'timeout' error, must be type int() ")

        for i in range(timeout_int):
            if elm is not None:
                if elm.is_displayed() is True:
                    break
                else:
                    sleep(1)
            else:
                sleep(1)
        else:
            raise TimeoutError("Timeout, element invisible")

