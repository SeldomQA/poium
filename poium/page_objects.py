import warnings
import platform
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from appium.webdriver.common.mobileby import MobileBy
from poium.common.exceptions import PageElementError
from poium.common.exceptions import FindElementTypesError
from poium.common import logging
from func_timeout import func_set_timeout
from func_timeout.exceptions import FunctionTimedOut
from poium.config import Browser


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
    'android_data_matcher': MobileBy.ANDROID_DATA_MATCHER,
    'android_view_matcher': MobileBy.ANDROID_VIEW_MATCHER,
    'windows_uiautomation': MobileBy.WINDOWS_UI_AUTOMATION,
    'accessibility_id': MobileBy.ACCESSIBILITY_ID,
    'image': MobileBy.IMAGE,
    'custom': MobileBy.CUSTOM,
}


class PageObject(object):
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


class Element(object):
    """
    Returns an element object
    """

    def __init__(self, timeout=5, describe="undefined", index=0, **kwargs):
        self.timeout = timeout
        self.index = index
        self.desc = describe
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST.keys():
            raise FindElementTypesError("Element positioning of type '{}' is not supported.".format(self.k))

    def __get__(self, instance, owner):
        if instance is None:
            return None

        Browser.driver = instance.driver
        return self

    def __set__(self, instance, value):
        self.__get__(instance, instance.__class__)
        self.send_keys(value)

    @func_set_timeout(0.5)
    def __elements(self, key, vlaue):
        elems = Browser.driver.find_elements(by=key, value=vlaue)
        return elems

    def __find_element(self, elem):
        """
        Find if the element exists.
        """
        for i in range(self.timeout):
            try:
                elems = self.__elements(elem[0], elem[1])
            except FunctionTimedOut:
                elems = []

            if len(elems) == 1:
                logging.info("✅ Find element: {by}={value} ".format(
                    by=elem[0], value=elem[1]))
                break
            elif len(elems) > 1:
                logging.info("❓ Find {n} elements through: {by}={value}".format(
                    n=len(elems), by=elem[0], value=elem[1]))
                break
            else:
                sleep(1)
        else:
            error_msg = "❌ Find 0 elements through: {by}={value}".format(by=elem[0], value=elem[1])
            logging.error(error_msg)
            raise NoSuchElementException(error_msg)

    def __get_element(self, by, value):
        """
        Judge element positioning way, and returns the element.
        """

        # selenium
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

        # appium
        elif by == "ios_uiautomation":
            self.__find_element((MobileBy.IOS_UIAUTOMATION, value))
            elem = Browser.driver.find_elements_by_ios_uiautomation(value)[self.index]
        elif by == "ios_predicate":
            self.__find_element((MobileBy.IOS_PREDICATE, value))
            elem = Browser.driver.find_elements_by_ios_predicate(value)[self.index]
        elif by == "ios_class_chain":
            self.__find_element((MobileBy.IOS_CLASS_CHAIN, value))
            elem = Browser.driver.find_elements_by_ios_class_chain(value)[self.index]
        elif by == "android_uiautomator":
            self.__find_element((MobileBy.ANDROID_UIAUTOMATOR, value))
            elem = Browser.driver.find_elements_by_android_uiautomator(value)[self.index]
        elif by == "android_viewtag":
            self.__find_element((MobileBy.ANDROID_VIEWTAG, value))
            elem = Browser.driver.find_elements_by_android_viewtag(value)[self.index]
        elif by == "android_data_matcher":
            self.__find_element((MobileBy.ANDROID_DATA_MATCHER, value))
            elem = Browser.driver.find_elements_by_android_data_matcher(value)[self.index]
        elif by == "accessibility_id":
            self.__find_element((MobileBy.ACCESSIBILITY_ID, value))
            elem = Browser.driver.find_elements_by_accessibility_id(value)[self.index]
        elif by == "android_view_matcher":
            self.__find_element((MobileBy.ANDROID_VIEW_MATCHER, value))
            elem = Browser.driver.find_elements_by_android_view_matcher(value)[self.index]
        elif by == "windows_uiautomation":
            self.__find_element((MobileBy.WINDOWS_UI_AUTOMATION, value))
            elem = Browser.driver.find_elements_by_windows_uiautomation(value)[self.index]
        elif by == "image":
            self.__find_element((MobileBy.IMAGE, value))
            elem = Browser.driver.find_elements_by_image(value)[self.index]
        elif by == "custom":
            self.__find_element((MobileBy.CUSTOM, value))
            elem = Browser.driver.find_elements_by_custom(value)[self.index]
        else:
            raise FindElementTypesError(
                "Please enter the correct targeting elements")
        if Browser.show is True:
            try:
                style_red = 'arguments[0].style.border="2px solid #FF0000"'
                style_blue = 'arguments[0].style.border="2px solid #00FF00"'
                style_null = 'arguments[0].style.border=""'

                for _ in range(2):
                    Browser.driver.execute_script(style_red, elem)
                    sleep(0.1)
                    Browser.driver.execute_script(style_blue, elem)
                    sleep(0.1)
                Browser.driver.execute_script(style_blue, elem)
                sleep(0.5)
                Browser.driver.execute_script(style_null, elem)
            except WebDriverException:
                pass

        return elem

    def clear(self):
        """Clears the text if it's a text entry element."""
        elem = self.__get_element(self.k, self.v)
        logging.info("clear element: {}".format(self.desc))
        elem.clear()

    def send_keys(self, value):
        """
        Simulates typing into the element.
        """
        elem = self.__get_element(self.k, self.v)
        logging.info("🖋 input element: {}".format(self.desc))
        elem.send_keys(value)

    def click(self):
        """Clicks the element."""
        elem = self.__get_element(self.k, self.v)
        logging.info("🖱 click element: {}".format(self.desc))
        elem.click()

    def submit(self):
        """Submits a form."""
        elem = self.__get_element(self.k, self.v)
        logging.info("submit element: {}".format(self.desc))
        elem.submit()

    @property
    def tag_name(self):
        """This element's ``tagName`` property."""
        elem = self.__get_element(self.k, self.v)
        return elem.tag_name

    @property
    def text(self):
        """Clears the text if it's a text entry element."""
        elem = self.__get_element(self.k, self.v)
        return elem.text

    @property
    def size(self):
        """The size of the element."""
        elem = self.__get_element(self.k, self.v)
        return elem.size

    def get_property(self, name):
        """
        Gets the given property of the element.
        """
        elem = self.__get_element(self.k, self.v)
        return elem.get_property(name)

    def get_attribute(self, name):
        """Gets the given attribute or property of the element."""
        elem = self.__get_element(self.k, self.v)
        return elem.get_attribute(name)

    def is_displayed(self):
        """Whether the element is visible to a user."""
        elem = self.__get_element(self.k, self.v)
        return elem.is_displayed()

    def is_selected(self):
        """
        Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
        """
        elem = self.__get_element(self.k, self.v)
        return elem.is_selected()

    def is_enabled(self):
        """Returns whether the element is enabled."""
        elem = self.__get_element(self.k, self.v)
        return elem.is_enabled()

    def switch_to_frame(self):
        """
        selenium API
        Switches focus to the specified frame
        """
        elem = self.__get_element(self.k, self.v)
        Browser.driver.switch_to.frame(elem)

    def move_to_element(self):
        """
        selenium API
        Moving the mouse to the middle of an element
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).move_to_element(elem).perform()

    def click_and_hold(self):
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).click_and_hold(elem).perform()

    def double_click(self):
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).double_click(elem).perform()

    def context_click(self):
        """
        selenium API
        Performs a context-click (right click) on an element.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).context_click(elem).perform()

    def drag_and_drop_by_offset(self, x, y):
        """
        selenium API
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.
        :param x: X offset to move to.
        :param y: Y offset to move to.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).drag_and_drop_by_offset(elem, xoffset=x, yoffset=y).perform()

    def refresh_element(self, timeout=10):
        """
        selenium API
        Refreshes the current page, retrieve elements.
        """
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError("Type 'timeout' error, must be type int() ")

        elem = self.__get_element(self.k, self.v)
        for i in range(timeout_int):
            if elem is not None:
                try:
                    elem
                except StaleElementReferenceException:
                    Browser.driver.refresh()
                else:
                    break
            else:
                sleep(1)
        else:
            raise TimeoutError("stale element reference: element is not attached to the page document.")

    def select_by_value(self, value):
        """
        selenium API
        Select all options that have a value matching the argument. That is, when given "foo" this
           would select an option like:

           <option value="foo">Bar</option>

           :Args:
            - value - The value to match against

           throws NoSuchElementException If there is no option with specisied value in SELECT
        """
        select_elem = self.__get_element(self.k, self.v)
        Select(select_elem).select_by_value(value)

    def select_by_index(self, index):
        """
        selenium API
        Select the option at the given index. This is done by examing the "index" attribute of an
           element, and not merely by counting.

           :Args:
            - index - The option at this index will be selected

           throws NoSuchElementException If there is no option with specisied index in SELECT
        """
        select_elem = self.__get_element(self.k, self.v)
        Select(select_elem).select_by_index(index)

    def select_by_visible_text(self, text):
        """
        selenium API
        Select all options that display text matching the argument. That is, when given "Bar" this
           would select an option like:

            <option value="foo">Bar</option>

           :Args:
            - text - The visible text to match against

            throws NoSuchElementException If there is no option with specisied text in SELECT
        """
        select_elem = self.__get_element(self.k, self.v)
        Select(select_elem).select_by_visible_text(text)

    def set_text(self, keys):
        """
        appium API
        Sends text to the element.
        """
        elem = self.__get_element(self.k, self.v)
        elem.set_text(keys)
        return self

    @property
    def location_in_view(self):
        """
        appium API
        Gets the location of an element relative to the view.
        Returns:
            dict: The location of an element relative to the view
        """
        elem = self.__get_element(self.k, self.v)
        return elem.location_in_view()

    def set_value(self, value):
        """
        appium API
        Set the value on this element in the application
        """
        elem = self.__get_element(self.k, self.v)
        elem.set_value(value)
        return self

    def input(self, text=""):
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(text)

    def enter(self):
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(Keys.ENTER)

    def select_all(self):
        elem = self.__get_element(self.k, self.v)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "a")
        else:
            elem.send_keys(Keys.CONTROL, "a")

    def cut(self):
        elem = self.__get_element(self.k, self.v)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "x")
        else:
            elem.send_keys(Keys.CONTROL, "x")

    def copy(self):
        elem = self.__get_element(self.k, self.v)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "c")
        else:
            elem.send_keys(Keys.CONTROL, "c")

    def paste(self):
        elem = self.__get_element(self.k, self.v)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "v")
        else:
            elem.send_keys(Keys.CONTROL, "v")

    def backspace(self):
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(Keys.BACKSPACE)

    def delete(self):
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(Keys.DELETE)

    def tab(self):
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(Keys.TAB)

    def space(self):
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(Keys.SPACE)


class Elements(object):
    """
    Returns a set of element objects
    """

    def __init__(self, context=False, describe="undefined", **kwargs):
        self.describe = describe
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        self.k, self.v = next(iter(kwargs.items()))
        try:
            self.locator = (LOCATOR_LIST[self.k], self.v)
        except KeyError:
            raise FindElementTypesError("Element positioning of type '{}' is not supported. ".format(self.k))
        self.has_context = bool(context)

    def find(self, context):
        try:
            elems = context.find_elements(*self.locator)
        except NoSuchElementException:
            elems = []
        logging.info("✨ Find {n} elements through: {by}={value}, describe:{desc}".format(
            n=len(elems), by=self.k, value=self.v, desc=self.describe))
        return elems

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
            raise PageElementError("Sorry, the set descriptor doesn't support elements with context.")
        elems = self.__get__(instance, instance.__class__)
        if not elems:
            raise PageElementError("Can't set value, no elements found")
        [elem.send_keys(value) for elem in elems]
