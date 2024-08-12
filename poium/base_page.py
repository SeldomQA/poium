"""
author：bugmaster

"""
import platform
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from poium import config
from poium.common import logging
from poium.common.exceptions import FuncTimeoutException
from poium.common.exceptions import PageElementError, FindElementTypesError, DriverNoneException
from poium.common.selector import selection_checker
from poium.config import Browser
from poium.libs.func_timeout import func_timeout

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
    'ios_predicate': AppiumBy.IOS_PREDICATE,
    'ios_class_chain': AppiumBy.IOS_CLASS_CHAIN,
    'android_uiautomator': AppiumBy.ANDROID_UIAUTOMATOR,
    'android_viewtag': AppiumBy.ANDROID_VIEWTAG,
    'android_data_matcher': AppiumBy.ANDROID_DATA_MATCHER,
    'android_view_matcher': AppiumBy.ANDROID_VIEW_MATCHER,
    'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
    'image': AppiumBy.IMAGE,
    'custom': AppiumBy.CUSTOM,
}

BY_LIST = [
    # selenium
    By.CSS_SELECTOR,
    By.ID,
    By.NAME,
    By.XPATH,
    By.LINK_TEXT,
    By.PARTIAL_LINK_TEXT,
    By.TAG_NAME,
    By.CLASS_NAME,
    # appium
    AppiumBy.IOS_PREDICATE,
    AppiumBy.IOS_CLASS_CHAIN,
    AppiumBy.ANDROID_UIAUTOMATOR,
    AppiumBy.ANDROID_VIEWTAG,
    AppiumBy.ANDROID_DATA_MATCHER,
    AppiumBy.ANDROID_VIEW_MATCHER,
    AppiumBy.ACCESSIBILITY_ID,
    AppiumBy.IMAGE,
    AppiumBy.CUSTOM
]


class BasePage:
    """
    Page Object pattern base class.
    """

    def __init__(self, driver=None, url: str = None, print_log: bool = False):
        """
        :param driver: `selenium.webdriver.WebDriver` Selenium webdriver instance
        :param url: `str`
        :param print_log: `bool` Need to be turned on when used with the seldom framework
        """
        self.driver = None
        if driver is not None:
            self.driver = driver
        else:
            try:
                # support seldom driver
                from seldom import Seldom
                if Seldom.driver is not None:
                    self.driver = Seldom.driver
                    print_log = True
            except ImportError:
                ...

        if self.driver is None:
            raise DriverNoneException("driver is None, Please set selenium/appium driver.")
        self.root_uri = url if url else getattr(self.driver, 'url', None)
        config.printLog = print_log

    def open(self, uri: str) -> None:
        """
        open uri
        :param uri: URI to GET, based off of the root_uri attribute.
        :return:
        """
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)
        self.driver.implicitly_wait(5)


class Element(object):
    """
    Returns an element object
    """

    def __init__(self, selector: str = None, timeout: int = 5, describe: str = "", index: int = 0, **kwargs):
        self.selector = selector
        self.times = timeout
        self.index = index
        self.desc = describe
        self.exist = False

        if selector is not None:
            self.by, self.value = selection_checker(selector)
        else:
            if not kwargs:
                raise ValueError("Please specify a locator")
            if len(kwargs) > 1:
                raise ValueError("Please specify only one locator")
            self.kwargs = kwargs
            self.by, self.value = next(iter(kwargs.items()))

            self.by = LOCATOR_LIST.get(self.by, None)
            if self.by is None:
                raise FindElementTypesError("Element positioning of type '{}' is not supported.".format(self.by))

    def __get__(self, instance, owner):
        if instance is None:
            return None

        self.driver = instance.driver
        return self

    def __set__(self, instance, value):
        self.__get__(instance, instance.__class__)
        self.send_keys(value)

    @func_timeout(1)
    def find_elements_timeout(self, by: str, value: str):
        """
        set find element timeout.
        :param by:
        :param value:
        :return:
        """
        return self.driver.find_elements(by, value)

    def find(self, by: str, value: str) -> list:
        """
        Find if the element exists.
        """
        for i in range(self.times):
            try:
                elems = self.find_elements_timeout(by, value)
                break
            except FuncTimeoutException:
                sleep(1)
        else:
            elems = []

        if len(elems) == 1:
            logging.info(f"🔍 Find element: {by}={value}. {self.desc}")
        elif len(elems) > 1:
            logging.info(f"❓ Find {len(elems)} elements through: {by}={value}. {self.desc}")
        else:
            logging.warning(f"❌ Find 0 elements through: {by}={value}. {self.desc}")

        return elems

    def get_element_object(self, by: str = None, value: str = None):
        """
        Judge element positioning way, and returns the element.
        """
        if by is None or value is None:
            by = self.by
            value = self.value

        if by not in BY_LIST:
            raise FindElementTypesError("Please enter the correct targeting elements")

        elems = self.find(by, value)
        if len(elems) == 0:
            self.exist = False
            return None
        else:
            self.exist = True
            elem = elems[self.index]

        if Browser.show is True:
            try:
                style_red = 'arguments[0].style.border="2px solid #FF0000"'
                style_blue = 'arguments[0].style.border="2px solid #00FF00"'
                style_null = 'arguments[0].style.border=""'

                for _ in range(2):
                    self.driver.execute_script(style_red, elem)
                    sleep(0.1)
                    self.driver.execute_script(style_blue, elem)
                    sleep(0.1)
                self.driver.execute_script(style_blue, elem)
                sleep(0.5)
                self.driver.execute_script(style_null, elem)
            except WebDriverException:
                pass

        return elem

    def is_exist(self) -> bool:
        """element is existed """
        self.get_element_object()
        return self.exist

    def clear(self) -> None:
        """Clears the text if it's a text entry element."""
        logging.info("✅ clear.")
        elem = self.get_element_object()
        elem.clear()

    def send_keys(self, value, clear=False, click=False) -> None:
        """
        Simulates typing into the element.
        If clear_before is True, it will clear the content before typing.
        """
        elem = self.get_element_object()
        if click is True:
            elem.click()
            sleep(0.5)
            logging.info(f"✅ click().")
        if clear is True:
            elem.clear()
            sleep(0.5)
            logging.info(f"✅ clear().")
        elem.send_keys(value)
        logging.info(f"✅ send_keys('{value}').")

    def click(self) -> None:
        """
        Clicks the element.
        """
        elem = self.get_element_object()
        elem.click()
        logging.info(f"✅ click().")

    def submit(self):
        """
        Submits a form.
        """
        elem = self.get_element_object()
        elem.submit()
        logging.info(f"✅ submit().")

    @property
    def tag_name(self) -> str:
        """This element's ``tagName`` property."""
        elem = self.get_element_object()
        tag_name = elem.tag_name
        logging.info(f"✅ tag_name: {tag_name}.")
        return tag_name

    @property
    def text(self) -> str:
        """The text of the element."""
        elem = self.get_element_object()
        text = elem.text
        logging.info(f"✅ text: {text}.")
        return text

    @property
    def size(self) -> dict:
        """The size of the element."""
        elem = self.get_element_object()
        size = elem.size
        logging.info(f"✅ size: {size}.")
        return size

    @property
    def location(self) -> dict:
        """The location of the element in the renderable canvas."""
        elem = self.get_element_object()
        loc = elem.location
        logging.info(f"✅ location: {loc}.")
        return loc

    @property
    def rect(self) -> dict:
        """A dictionary with the size and location of the element."""
        elem = self.get_element_object()
        rect = elem.rect
        logging.info(f"✅ rect: {rect}.")
        return rect

    @property
    def aria_role(self) -> str:
        """Returns the ARIA role of the current web element."""
        elem = self.get_element_object()
        aria_role = elem.aria_role
        logging.info(f"✅ aria_role: {aria_role}.")
        return aria_role

    @property
    def accessible_name(self) -> str:
        """Returns the ARIA Level of the current webelement."""
        elem = self.get_element_object()
        accessible_name = elem.accessible_name
        logging.info(f"✅ accessible_name: {accessible_name}.")
        return accessible_name

    def screenshot(self, filename: str = None):
        """
        element screenshot.
        :param filename:
        :return:
        """
        elem = self.get_element_object()
        if filename is not None:
            result = elem.screenshot(filename)
            logging.info(f"✅ screenshot save to: {filename}.")
            return result

        b64 = elem.screenshot_as_png
        logging.info(f"✅ screenshot save base64.")
        return b64

    def value_of_css_property(self, property_name):
        """
        The value of a CSS property
        :param property_name:
        """
        elem = self.get_element_object()
        property_value = elem.value_of_css_property(property_name)
        logging.info(f"✅ value_of_css_property('{property_name}') -> {property_value}.")
        return property_value

    def get_property(self, name) -> str:
        """
        Gets the given property of the element.
        """
        elem = self.get_element_object()
        value = elem.get_property(name)
        logging.info(f"✅ get_property('{name}') -> {value}.")
        return value

    def get_dom_attribute(self, name) -> str:
        """Gets the given attribute of the element."""
        elem = self.get_element_object()
        value = elem.get_dom_attribute(name)
        logging.info(f"✅ get_dom_attribute('{name}') -> {value}.")
        return value

    def get_attribute(self, name) -> str:
        """
        Gets the given attribute or property of the element.
        """
        elem = self.get_element_object()
        value = elem.get_attribute(name)
        logging.info(f"✅ get_attribute('{name}') -> {value}.")
        return value

    def is_displayed(self) -> bool:
        """Whether the element is visible to a user."""
        elem = self.get_element_object()
        display = elem.is_displayed()
        logging.info(f"✅ is_displayed() -> {display}.")
        return display

    def is_selected(self) -> bool:
        """
        Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
        """
        elem = self.get_element_object()
        select = elem.is_selected()
        logging.info(f"✅ is_selected() -> {select}.")
        return select

    def is_enabled(self) -> bool:
        """Returns whether the element is enabled."""
        elem = self.get_element_object()
        enable = elem.is_enabled()
        logging.info(f"✅ is_enabled() -> {enable}.")
        return enable

    def switch_to_frame(self) -> None:
        """
        selenium API
        Switches focus to the specified frame
        """
        elem = self.get_element_object()
        self.driver.switch_to.frame(elem)
        logging.info(f"✅ switch_to_frame().")

    def frame(self) -> None:
        """
        selenium API
        Switches focus to the specified frame
        """
        return self.switch_to_frame()

    def move_to_element(self) -> None:
        """
        selenium API
        Moving the mouse to the middle of an element
        """
        elem = self.get_element_object()
        ActionChains(self.driver).move_to_element(elem).perform()
        logging.info(f"✅ move_to_element().")

    def click_and_hold(self) -> None:
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        elem = self.get_element_object()
        ActionChains(self.driver).click_and_hold(elem).perform()
        logging.info(f"✅ click_and_hold().")

    def double_click(self) -> None:
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        elem = self.get_element_object()
        ActionChains(self.driver).double_click(elem).perform()
        logging.info(f"✅ double_click().")

    def context_click(self) -> None:
        """
        selenium API
        Performs a context-click (right click) on an element.
        """
        elem = self.get_element_object()
        ActionChains(self.driver).context_click(elem).perform()
        logging.info(f"✅ context_click().")

    def drag_and_drop_by_offset(self, x: int, y: int) -> None:
        """
        selenium API
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.
        :param x: X offset to move to.
        :param y: Y offset to move to.
        """
        elem = self.get_element_object()
        ActionChains(self.driver).drag_and_drop_by_offset(elem, xoffset=x, yoffset=y).perform()
        logging.info(f"✅ drag_and_drop_by_offset('{x}', '{y}').")

    def refresh_element(self, timeout: int = 10) -> None:
        """
        selenium API
        Refreshes the current page, retrieve elements.
        """
        elem = self.get_element_object()
        for i in range(timeout):
            if elem is not None:
                try:
                    elem
                except StaleElementReferenceException:
                    self.driver.refresh()
                else:
                    break
            else:
                sleep(1)
        else:
            raise TimeoutError("stale element reference: element is not attached to the page document.")

    def select_by_value(self, value: str) -> None:
        """
        selenium API
        Select all options that have a value matching the argument. That is, when given "foo" this
           would select an option like:

           <option value="foo">Bar</option>

           :Args:
            - value - The value to match against

           throws NoSuchElementException If there is no option with specisied value in SELECT
        """
        select_elem = self.get_element_object()
        Select(select_elem).select_by_value(value)
        logging.info(f"✅ select_by_value('{value}').")

    def select_by_index(self, index: int) -> None:
        """
        selenium API
        Select the option at the given index. This is done by examing the "index" attribute of an
           element, and not merely by counting.

           :Args:
            - index - The option at this index will be selected

           throws NoSuchElementException If there is no option with specisied index in SELECT
        """
        select_elem = self.get_element_object()
        Select(select_elem).select_by_index(index)
        logging.info(f"✅ select_by_index('{index}').")

    def select_by_visible_text(self, text: str) -> None:
        """
        selenium API
        Select all options that display text matching the argument. That is, when given "Bar" this
           would select an option like:

            <option value="foo">Bar</option>

           :Args:
            - text - The visible text to match against

            throws NoSuchElementException If there is no option with specisied text in SELECT
        """
        select_elem = self.get_element_object()
        Select(select_elem).select_by_visible_text(text)
        logging.info(f"✅ select_by_visible_text('{text}').")

    def set_text(self, keys):
        """
        appium API
        Sends text to the element.
        """
        elem = self.get_element_object()
        elem.set_text(keys)
        logging.info(f"✅ set_text('{keys}').")
        return self

    @property
    def location_in_view(self):
        """
        appium API
        Gets the location of an element relative to the view.
        Returns:
            dict: The location of an element relative to the view
        """
        elem = self.get_element_object()
        location = elem.location_in_view
        logging.info(f"✅ location_in_view -> {location}.")
        return location

    def set_value(self, value: str):
        """
        appium API
        Set the value on this element in the application
        """
        elem = self.get_element_object()
        elem.set_value(value)
        logging.info(f"✅ set_value('{value}').")
        return self

    def input(self, text="") -> None:
        """
        input.
        :param text:
        :return:
        """
        elem = self.get_element_object()
        elem.send_keys(text)
        logging.info(f"🎹 input('{text}').")

    def enter(self) -> None:
        """
        Enter key
        :return:
        """
        elem = self.get_element_object()
        elem.send_keys(Keys.ENTER)
        logging.info(f"🎹 enter.")

    def select_all(self) -> None:
        """
        select all.
        :return:
        """
        elem = self.get_element_object()
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "a")
        else:
            elem.send_keys(Keys.CONTROL, "a")
        logging.info(f"🎹 control + a.")

    def cut(self) -> None:
        """
        cut.
        :return:
        """
        elem = self.get_element_object()
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "x")
        else:
            elem.send_keys(Keys.CONTROL, "x")
        logging.info(f"🎹 control + x.")

    def copy(self) -> None:
        """
        copy
        :return:
        """
        elem = self.get_element_object()
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "c")
        else:
            elem.send_keys(Keys.CONTROL, "c")
        logging.info(f"🎹 control + c.")

    def paste(self) -> None:
        """
        paste.
        :return:
        """
        elem = self.get_element_object()
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "v")
        else:
            elem.send_keys(Keys.CONTROL, "v")
        logging.info(f"🎹 control + v.")

    def backspace(self) -> None:
        """
        Backspace key.
        :return:
        """
        elem = self.get_element_object()
        elem.send_keys(Keys.BACKSPACE)
        logging.info(f"🎹 backspace.")

    def delete(self) -> None:
        """
        Delete key.
        :return:
        """
        elem = self.get_element_object()
        elem.send_keys(Keys.DELETE)
        logging.info(f"🎹 delete.")

    def tab(self) -> None:
        """
        Tab key.
        :return:
        """
        elem = self.get_element_object()
        elem.send_keys(Keys.TAB)
        logging.info(f"🎹 tab.")

    def space(self) -> None:
        """
        Space key.
        :return:
        """
        elem = self.get_element_object()
        elem.send_keys(Keys.SPACE)
        logging.info(f"🎹 space.")


class Elements(object):
    """
    Returns a set of element objects
    """

    def __init__(self, selector: str = None, context: bool = False, describe: str = "", timeout: int = 5, **kwargs):
        self.desc = describe
        self.times = timeout
        if selector is not None:
            self.by, self.value = selection_checker(selector)
        else:
            if not kwargs:
                raise ValueError("Please specify a locator")
            if len(kwargs) > 1:
                raise ValueError("Please specify only one locator")
            by, self.value = next(iter(kwargs.items()))

            self.by = LOCATOR_LIST.get(by, None)
            if self.by is None:
                raise FindElementTypesError("Element positioning of type '{}' is not supported.".format(self.by))

        self.has_context = bool(context)

    def find(self, context):
        """
        find element.
        :param context:
        :return:
        """
        for i in range(self.times):
            elems = context.find_elements(self.by, self.value)
            if len(elems) > 0:
                break
            else:
                sleep(1)
        else:
            elems = []

        logging.info(f"✨ Find {len(elems)} elements through: {self.by}={self.value}. {self.desc}")
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
