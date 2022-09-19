import warnings
import platform
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from appium.webdriver.common.appiumby import AppiumBy
from poium.common.exceptions import PageElementError
from poium.common.exceptions import FindElementTypesError
from poium.common import logging
from func_timeout import func_set_timeout
from func_timeout.exceptions import FunctionTimedOut
from poium import config
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
    'ios_uiautomation': AppiumBy.IOS_UIAUTOMATION,
    'ios_predicate': AppiumBy.IOS_PREDICATE,
    'ios_class_chain': AppiumBy.IOS_CLASS_CHAIN,
    'android_uiautomator': AppiumBy.ANDROID_UIAUTOMATOR,
    'android_viewtag': AppiumBy.ANDROID_VIEWTAG,
    'android_data_matcher': AppiumBy.ANDROID_DATA_MATCHER,
    'android_view_matcher': AppiumBy.ANDROID_VIEW_MATCHER,
    'windows_uiautomation': AppiumBy.WINDOWS_UI_AUTOMATION,
    'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
    'image': AppiumBy.IMAGE,
    'custom': AppiumBy.CUSTOM,
}


class PageBase(object):
    """
    Page Object pattern.
    """

    def __init__(self, driver, url=None,  print_log: bool = False):
        """
        :param driver: `selenium.webdriver.WebDriver` Selenium webdriver instance
        :param url: `str`
        :param print_log: `bool` Need to be turned on when used with the seldom framework
        Root URI to base any calls to the ``PageObject.get`` method. If not defined
        in the constructor it will try and look it from the webdriver object.
        """
        self.driver = driver
        self.root_uri = url if url else getattr(self.driver, 'url', None)
        config.printLog = print_log

    def get(self, uri):
        """
        :param uri:  URI to GET, based off of the root_uri attribute.
        """
        warnings.warn("use page.open() instead",
                      DeprecationWarning, stacklevel=2)
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)
        self.driver.implicitly_wait(5)

    def open(self, uri):
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

    def __init__(self, timeout: int = 5, describe: str = "", index: int = 0, **kwargs):
        self.times = timeout
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

    @func_set_timeout(1)
    def __elements(self, key, vlaue):
        elems = Browser.driver.find_elements(key, vlaue)
        return elems

    def __find_element(self, elem):
        """
        Find if the element exists.
        """
        for i in range(self.times):
            try:
                elems = self.__elements(elem[0], elem[1])
            except FunctionTimedOut:
                elems = []

            if len(elems) == 1:
                logging.info(f"🔍 Find element: {elem[0]}={elem[1]}. {self.desc}")
                break
            elif len(elems) > 1:
                logging.info(f"❓ Find {len(elems)} elements through: {elem[0]}={elem[1]}. {self.desc}")
                break
            else:
                sleep(1)
        else:
            logging.warning(f"❌ Find 0 elements through: {elem[0]}={elem[1]}. {self.desc}")

    def __get_element(self, by, value):
        """
        Judge element positioning way, and returns the element.
        """

        # selenium
        if by == "id_":
            self.__find_element((By.ID, value))
            elem = Browser.driver.find_elements(By.ID, value)[self.index]
        elif by == "name":
            self.__find_element((By.NAME, value))
            elem = Browser.driver.find_elements(By.NAME, value)[self.index]
        elif by == "class_name":
            self.__find_element((By.CLASS_NAME, value))
            elem = Browser.driver.find_elements(By.CLASS_NAME, value)[self.index]
        elif by == "tag":
            self.__find_element((By.TAG_NAME, value))
            elem = Browser.driver.find_elements(By.TAG_NAME, value)[self.index]
        elif by == "link_text":
            self.__find_element((By.LINK_TEXT, value))
            elem = Browser.driver.find_elements(By.LINK_TEXT, value)[self.index]
        elif by == "partial_link_text":
            self.__find_element((By.PARTIAL_LINK_TEXT, value))
            elem = Browser.driver.find_elements(By.PARTIAL_LINK_TEXT, value)[self.index]
        elif by == "xpath":
            self.__find_element((By.XPATH, value))
            elem = Browser.driver.find_elements(By.XPATH, value)[self.index]
        elif by == "css":
            self.__find_element((By.CSS_SELECTOR, value))
            elem = Browser.driver.find_elements(By.CSS_SELECTOR, value)[self.index]

        # appium
        elif by == "ios_uiautomation":
            self.__find_element((AppiumBy.IOS_UIAUTOMATION, value))
            elem = Browser.driver.find_elements(AppiumBy.IOS_UIAUTOMATION, value)[self.index]
        elif by == "ios_predicate":
            self.__find_element((AppiumBy.IOS_PREDICATE, value))
            elem = Browser.driver.find_elements(AppiumBy.IOS_PREDICATE, value)[self.index]
        elif by == "ios_class_chain":
            self.__find_element((AppiumBy.IOS_CLASS_CHAIN, value))
            elem = Browser.driver.find_elements(AppiumBy.IOS_CLASS_CHAIN, value)[self.index]
        elif by == "android_uiautomator":
            self.__find_element((AppiumBy.ANDROID_UIAUTOMATOR, value))
            elem = Browser.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, value)[self.index]
        elif by == "android_viewtag":
            self.__find_element((AppiumBy.ANDROID_VIEWTAG, value))
            elem = Browser.driver.find_elements(AppiumBy.ANDROID_VIEWTAG, value)[self.index]
        elif by == "android_data_matcher":
            self.__find_element((AppiumBy.ANDROID_DATA_MATCHER, value))
            elem = Browser.driver.find_elements(AppiumBy.ANDROID_DATA_MATCHER, value)[self.index]
        elif by == "accessibility_id":
            self.__find_element((AppiumBy.ACCESSIBILITY_ID, value))
            elem = Browser.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, value)[self.index]
        elif by == "android_view_matcher":
            self.__find_element((AppiumBy.ANDROID_VIEW_MATCHER, value))
            elem = Browser.driver.find_elements(AppiumBy.ANDROID_VIEW_MATCHER, value)[self.index]
        elif by == "windows_uiautomation":
            self.__find_element((AppiumBy.WINDOWS_UI_AUTOMATION, value))
            elem = Browser.driver.find_elements(AppiumBy.WINDOWS_UI_AUTOMATION, value)[self.index]
        elif by == "image":
            self.__find_element((AppiumBy.IMAGE, value))
            elem = Browser.driver.find_elements(AppiumBy.IMAGE, value)[self.index]
        elif by == "custom":
            self.__find_element((AppiumBy.CUSTOM, value))
            elem = Browser.driver.find_elements(AppiumBy.CUSTOM, value)[self.index]
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
        logging.info("✅ clear.")
        elem = self.__get_element(self.k, self.v)
        elem.clear()

    def send_keys(self, value, clear=False, click=False) -> None:
        """
        Simulates typing into the element.
        If clear_before is True, it will clear the content before typing.
        """
        elem = self.__get_element(self.k, self.v)
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
        elem = self.__get_element(self.k, self.v)
        elem.click()
        logging.info(f"✅ click().")

    def submit(self):
        """
        Submits a form.
        """
        elem = self.__get_element(self.k, self.v)
        elem.submit()
        logging.info(f"✅ submit().")

    @property
    def tag_name(self) -> str:
        """This element's ``tagName`` property."""
        elem = self.__get_element(self.k, self.v)
        tag_name = elem.tag_name
        logging.info(f"✅ tag_name: {tag_name}.")
        return tag_name

    @property
    def text(self) -> str:
        """The text of the element."""
        elem = self.__get_element(self.k, self.v)
        text = elem.text
        logging.info(f"✅ text: {text}.")
        return text

    @property
    def size(self) -> dict:
        """The size of the element."""
        elem = self.__get_element(self.k, self.v)
        size = elem.size
        logging.info(f"✅ size: {size}.")
        return size

    def value_of_css_property(self, property_name):
        """
        The value of a CSS property
        :param property_name:
        """
        elem = self.__get_element(self.k, self.v)
        property_value = elem.value_of_css_property(property_name)
        logging.info(f"✅ value_of_css_property('{property_name}') -> {property_value}.")
        return property_value

    def get_property(self, name) -> str:
        """
        Gets the given property of the element.
        """
        elem = self.__get_element(self.k, self.v)
        value = elem.get_property(name)
        logging.info(f"✅ get_property('{name}') -> {value}.")
        return value

    def get_attribute(self, name) -> str:
        """
        Gets the given attribute or property of the element.
        """
        elem = self.__get_element(self.k, self.v)
        value = elem.get_attribute(name)
        logging.info(f"✅ get_property('{name}') -> {value}.")
        return value

    def is_displayed(self) -> bool:
        """Whether the element is visible to a user."""
        elem = self.__get_element(self.k, self.v)
        display = elem.is_displayed()
        logging.info(f"✅ is_displayed() -> {display}.")
        return display

    def is_selected(self):
        """
        Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
        """
        elem = self.__get_element(self.k, self.v)
        select = elem.is_selected()
        logging.info(f"✅ is_selected() -> {select}.")
        return select

    def is_enabled(self):
        """Returns whether the element is enabled."""
        elem = self.__get_element(self.k, self.v)
        enable = elem.is_enabled()
        logging.info(f"✅ is_enabled() -> {enable}.")
        return enable

    def switch_to_frame(self) -> None:
        """
        selenium API
        Switches focus to the specified frame
        """
        elem = self.__get_element(self.k, self.v)
        Browser.driver.switch_to.frame(elem)
        logging.info(f"✅ switch_to_frame().")

    def move_to_element(self) -> None:
        """
        selenium API
        Moving the mouse to the middle of an element
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).move_to_element(elem).perform()
        logging.info(f"✅ move_to_element().")

    def click_and_hold(self) -> None:
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).click_and_hold(elem).perform()
        logging.info(f"✅ click_and_hold().")

    def double_click(self) -> None:
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).double_click(elem).perform()
        logging.info(f"✅ double_click().")

    def context_click(self) -> None:
        """
        selenium API
        Performs a context-click (right click) on an element.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).context_click(elem).perform()
        logging.info(f"✅ double_click().")

    def drag_and_drop_by_offset(self, x: int, y: int) -> None:
        """
        selenium API
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.
        :param x: X offset to move to.
        :param y: Y offset to move to.
        """
        elem = self.__get_element(self.k, self.v)
        ActionChains(Browser.driver).drag_and_drop_by_offset(elem, xoffset=x, yoffset=y).perform()
        logging.info(f"✅ drag_and_drop_by_offset('{x}', '{y}').")

    def refresh_element(self, timeout: int = 10) -> None:
        """
        selenium API
        Refreshes the current page, retrieve elements.
        """
        elem = self.__get_element(self.k, self.v)
        for i in range(timeout):
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
        select_elem = self.__get_element(self.k, self.v)
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
        select_elem = self.__get_element(self.k, self.v)
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
        select_elem = self.__get_element(self.k, self.v)
        Select(select_elem).select_by_visible_text(text)
        logging.info(f"✅ select_by_visible_text('{text}').")

    def set_text(self, keys):
        """
        appium API
        Sends text to the element.
        """
        elem = self.__get_element(self.k, self.v)
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
        elem = self.__get_element(self.k, self.v)
        location = elem.location_in_view()
        logging.info(f"✅ location_in_view -> {location}.")
        return location

    def set_value(self, value: str):
        """
        appium API
        Set the value on this element in the application
        """
        elem = self.__get_element(self.k, self.v)
        elem.set_value(value)
        logging.info(f"✅ set_value('{value}').")
        return self

    def input(self, text="") -> None:
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(text)
        logging.info(f"🎹 input('{text}').")

    def enter(self) -> None:
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(Keys.ENTER)
        logging.info(f"🎹 enter.")

    def select_all(self) -> None:
        elem = self.__get_element(self.k, self.v)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "a")
        else:
            elem.send_keys(Keys.CONTROL, "a")
        logging.info(f"🎹 control + a.")

    def cut(self) -> None:
        elem = self.__get_element(self.k, self.v)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "x")
        else:
            elem.send_keys(Keys.CONTROL, "x")
        logging.info(f"🎹 control + x.")

    def copy(self) -> None:
        elem = self.__get_element(self.k, self.v)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "c")
        else:
            elem.send_keys(Keys.CONTROL, "c")
        logging.info(f"🎹 control + c.")

    def paste(self) -> None:
        elem = self.__get_element(self.k, self.v)
        if platform.system().lower() == "darwin":
            elem.send_keys(Keys.COMMAND, "v")
        else:
            elem.send_keys(Keys.CONTROL, "v")
        logging.info(f"🎹 control + v.")

    def backspace(self) -> None:
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(Keys.BACKSPACE)
        logging.info(f"🎹 backspace.")

    def delete(self) -> None:
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(Keys.DELETE)
        logging.info(f"🎹 delete.")

    def tab(self) -> None:
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(Keys.TAB)
        logging.info(f"🎹 tab.")

    def space(self) -> None:
        elem = self.__get_element(self.k, self.v)
        elem.send_keys(Keys.SPACE)
        logging.info(f"🎹 space.")


class Elements(object):
    """
    Returns a set of element objects
    """

    def __init__(self, context=False, describe: str = "", timeout: int = 5, **kwargs):
        self.desc = describe
        self.times = timeout
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        self.k, self.v = next(iter(kwargs.items()))
        try:
            self.locator = (LOCATOR_LIST[self.k], self.v)
        except KeyError:
            raise FindElementTypesError(f"Element positioning of type '{self.k}' is not supported. ")
        self.has_context = bool(context)

    def find(self, context):
        for i in range(self.times):
            elems = context.find_elements(*self.locator)
            if len(elems) == 0:
                sleep(1)
            else:
                break
        else:
            elems = []
            logging.info(f"✨ Find {len(elems)} elements through: {self.k}={self.v}. {self.desc}")
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
