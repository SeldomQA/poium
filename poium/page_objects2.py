import logging
import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from poium.common.exceptions import PageSelectException
from poium.common.exceptions import PageElementError
from poium.common.exceptions import FindElementTypesError

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


class Browser:
    driver = None


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

    def run_script(self, js=None, *args):
        """
        run JavaScript script
        """
        if js is None:
            raise ValueError("Please input js script")
        else:
            self.driver.execute_script(js, *args)


class PageElement(object):

    def __init__(self, timeout=10, describe=None, index=0, **kwargs):
        self.timeout = timeout
        self.index = index
        if not kwargs:
            raise ValueError("Please specify a locator")
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST:
            raise KeyError("Element positioning of type '{}' is not supported.".format(self.k))

    def __get__(self, instance, owner):

        if instance is None:
            return None

        Browser.driver = instance.driver
        return self

    def __find_element(self, elem):
        """
        Find if the element exists.
        """
        for i in range(self.timeout):
            elems = Browser.driver.find_elements(by=elem[0], value=elem[1])
            if len(elems) == 1:
                print("Find element: {by}={value} ".format(by=elem[0], value=elem[1]))
                break
            elif len(elems) > 1:
                print("Find {n} elements through：{by}={value}".format(n=len(elems), by=elem[0], value=elem[1]))
                break
            else:
                time.sleep(1)
        else:
            print("Find 0 elements through：{by}={value}".format(by=elem[0], value=elem[1]))

    def __get_element(self, by, value):
        """
        Judge element positioning way, and returns the element.
        """

        if by == "id_":
            self.__find_element((By.ID, value))
            elem = Browser.driver.find_elements_by_id(value)[self.index]
        elif by == "name":
            self.__find_element((By.NAME, value))
            elem = Browser.driver.find_elements_by_name(value)[self.index]
        elif by == "class_name":
            self.__find_element((By.CLASS_NAME, value))
            elem = Browser.driver.find_elements_by_class_name(value)[self.index]
        elif by == "tag":
            self.__find_element((By.TAG_NAME, value))
            elem = Browser.driver.find_elements_by_tag_name(value)[self.index]
        elif by == "link_text":
            self.__find_element((By.LINK_TEXT, value))
            elem = Browser.driver.find_elements_by_link_text(value)[self.index]
        elif by == "partial_link_text":
            self.__find_element((By.PARTIAL_LINK_TEXT, value))
            elem = Browser.driver.find_elements_by_partial_link_text(value)[self.index]
        elif by == "xpath":
            self.__find_element((By.XPATH, value))
            elem = Browser.driver.find_elements_by_xpath(value)[self.index]
        elif by == "css":
            self.__find_element((By.CSS_SELECTOR, value))
            elem = Browser.driver.find_elements_by_css_selector(value)[self.index]
        else:
            raise NameError(
                "Please enter the correct targeting elements,'id_/name/class_name/tag/link_text/xpath/css'.")
        return elem

    def send_keys(self, value):
        """
        send_keys()
        :param value:
        :return:
        """
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(value)

    def click(self):
        """
        click()
        :return:
        """
        elem = self.__get_element(self.k, self.v)
        elem.click()
