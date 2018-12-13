from time import sleep
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

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
    'class_': By.CLASS_NAME,
    # appium
    'ios_uiautomation': MobileBy.IOS_UIAUTOMATION,
    'ios_predicate': MobileBy.IOS_PREDICATE,
    'ios_class_chain': MobileBy.IOS_CLASS_CHAIN,
    'android_uiautomator': MobileBy.ANDROID_UIAUTOMATOR,
    'accessibility_id': MobileBy.ACCESSIBILITY_ID,
    'image': MobileBy.IMAGE,
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

    def window_scroll(self, width=None, height=None):
        """
        Setting width and height of window scroll bar.
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = "window.scrollTo({w},{h});".format(w=width, h=height)
        self.run_script(js)

    def switch_to_frame(self, frame_reference):
        """
        Switches focus to the specified frame, by id, name, or webelement.
        """
        self.driver.switch_to.frame(frame_reference)

    def switch_to_frame_out(self):
        """
        Switches focus to the parent context.
        Corresponding relationship with switch_to_frame () method.
        """
        self.driver.switch_to.parent_frame()

    def accept_alert(self):
        """
        Accept warning box.
        """
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        Dismisses the alert available.
        """
        self.driver.switch_to.alert.dismiss()

    @property
    def get_alert_text(self):
        """
        Get warning box prompt information.
        """
        return self.driver.switch_to.alert.text

    @property
    def get_title(self):
        """
        Get window title.
        Usage:
        driver.get_title()
        """
        return self.driver.title

    @property
    def get_url(self):
        """
        Get the URL address of the current page.
        Usage:
        driver.get_url()
        """
        return self.driver.current_url

    def move_to_element(self, elem):
        """
        Moving the mouse to the middle of an element
        """
        ActionChains(self.driver).move_to_element(elem).perform()

    def context_click(self, elem):
        """
        Performs a context-click (right click) on an element.
        """
        ActionChains(self.driver).context_click(elem).perform()

    def drag_and_drop_by_offset(self, elem, x, y):
        """
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.
        :param elem: The element to mouse down.
        :param x: X offset to move to.
        :param y: Y offset to move to.
        """
        ActionChains(self.driver).drag_and_drop_by_offset(elem, xoffset=x, yoffset=y).perform()

    def refresh_element(self, elem, timeout=10):
        """
        Refreshes the current page, retrieve elements.
        """
        try:
            timeout_int = int(timeout)
        except TypeError:
            raise ValueError("Type 'timeout' error, must be type int() ")

        for i in range(timeout_int):
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
        >> from page_objects import PageObject, PageElement
        >> class MyPage(PageObject):
                elem1 = PageElement(css='div.myclass')
                elem2 = PageElement(id_='foo')
                elem_with_context = PageElement(name='bar', context=True)
    Page Elements act as property descriptors for their Page Object, you can get
    and set them as normal attributes.
    """
    def __init__(self, context=False, timeout=10, describe=None, **kwargs):
        self.time_out = timeout
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        k, v = next(iter(kwargs.items()))
        try:
            self.locator = (LOCATOR_LIST[k], v)
        except KeyError:
            raise KeyError("Please use a locator：'id_'、'name'、'class_'、'css'、'xpath'、'link_text'、'partial_link_text'.")
        self.has_context = bool(context)

    def get_element(self, context):
        try:
            return context.find_element(*self.locator)
        except NoSuchElementException:
            return None

    def find(self, context):
        for i in range(self.time_out):
            if self.get_element(context) is not None:
                return self.get_element(context)
            else:
                sleep(1)
        else:
            return None

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
    >> from page_objects import PageObject, PageElements
    >> class MyPage(PageObject):
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


# Backwards compatibility with previous versions that used factory methods
page_element = PageElement
page_elements = PageElements

