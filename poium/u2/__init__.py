import time
from typing import Union

from poium.common import logging
from poium.common.openatx import BasePage

LOCATOR_LIST = [
    "text",
    "textContains",
    "textMatches",
    "textStartsWith",
    "className",
    "classNameMatches",
    "description",
    "descriptionContains",
    "descriptionMatches",
    "descriptionStartsWith",
    "checkable",
    "checked",
    "clickable",
    "longClickable",
    "scrollable",
    "enabled",
    "focusable",
    "focused",
    "selected",
    "packageName",
    "packageNameMatches",
    "resourceId",
    "resourceIdMatches",
    "index",
    "instance",
]


class Page(BasePage):
    """
    uiautomator2 page class
    """

    def window_size(self):
        """
        Resolution size
        :return: (width, height)
        """
        size = self.driver.window_size()
        logging.info(f"📱 window high: {size[1]} wight: {size[0]}")
        return size

    def app_list(self) -> list:
        """
        Get app list
        :return:
        """
        logging.info(f"📱 app list")
        return self.driver.app_list()

    def app_info(self, package_name=None):
        """
        Get app info
        :param package_name:
        :return:
        """
        if package_name is not None:
            pkg = package_name
        elif self.package_name is not None:
            pkg = self.package_name
        else:
            raise NameError("package name is None")

        logging.info(f"📱 app info: {pkg}")
        return self.driver.app_info(pkg)

    def click(self, x: float = None, y: float = None, text: str = None):
        """
        click position
        :param x:
        :param y:
        :param text:
        :return:
        """
        if not x and not y and not text:
            raise ValueError
        (x, y) = self.driver(text=text).center() if text else (x, y)

        logging.info(f"👆 click: {x}, {y}")

        self.driver.click(x, y)

    def click_more(self, x, y, sleep=0, times=3):
        """
        Multiple clicks.
        :param x:
        :param y:
        :param sleep: interval time
        :param times: click times
        :return:
        """
        w, h = self.window_size()
        x, y = (w * x, h * y) if x < 1 and y < 1 else x, y

        logging.info(f"👆 click {times} times: {x}, {y}")

        for _ in range(times):
            self.driver.touch.down(x, y)
            self.sleep(sleep)
            self.driver.touch.up(x, y)

    def swipe(self, fx: float, fy: float, tx: float, ty: float, duration: float = 0, steps=None, times: int = 1,
              orientation: str = ""):
        """
        UiAutoMatTor use steps instead of duration
          As the document say: Each step execution is throttled to 5ms per step.
        :param fx:
        :param fy:
        :param tx:
        :param ty:
        :param duration:
        :param steps: 1 step is about 5ms, if set, duration will be ignored
        :param times:
        :param orientation:
        :return:
        """
        logging.info(f"👆 {orientation} swipe: [{fx}, {fy}] => [{tx}, {ty}], times: {times} ")
        for _ in range(times):
            self.driver.swipe(fx, fy, tx, ty, duration, steps)
            self.sleep(1)

    def swipe_search(self, text: str, direction: str = "up", x: float = None, y: float = None):
        """
        swipe search text
        :param text:
        :param direction: "down" or "up"
        :param x:
        :param y:
        :return:
        """
        logging.info(f"🔍 swipe search: {text}")
        x = 0.5 if not x else x
        y = 0.5 if not y else y
        for i in range(20):
            if self.driver(textContains=text).exists:
                break
            else:
                if direction == "down":
                    self.swipe_down(fx=x, fy=y, tx=x, ty=y - 0.2)
                elif direction == "up":
                    self.swipe_up(fx=x, fy=y, tx=x, ty=y + 0.2)
                else:
                    raise NameError(f"direction {direction} error.")
        else:
            raise TimeoutError("Timeout, element not found")

    def press(self, key: Union[int, str], meta=None):
        """
        Documents:
            press key via name or key code. Supported key name includes:
            home, back, left, right, up, down, center, menu, search, enter,
            delete(or del), recent(recent apps), volume_up, volume_down,
            volume_mute, camera, power.
        """
        logging.info(f"👆 press: {key}")
        self.driver.press(key, meta=meta)


class XpathElement(object):
    """
    Only CSS selectors are supported.
    https://github.com/openatx/uiautomator2/blob/master/XPATH.md

    >> from poium.u2 import Page, XpathElement
    >> class MyPage(Page):
            input = XpathElement('//android.widget.EditText')
            button = XpathElement('@com.taobao.taobao:id/fl_banner_container')
    """

    def __init__(self, xpath: str, index: int = None, timeout: int = 10, describe: str = None):
        self.xpath = xpath
        self.describe = describe
        self.timeout = timeout
        if index is None:
            self.index = 0
        self.desc = describe

    def __get__(self, instance, owner):
        if instance is None:
            return None
        self.driver = instance.driver
        return self

    def click(self):
        """
        Click element.
        """
        self.driver.xpath(self.xpath).click()
        logging.info(f"✅ Xpath:{self.xpath}, click().")

    def set_text(self, value):
        """
        Simulates typing into the element.
        :param value: input text
        """
        self.driver.xpath(self.xpath).set_text(value)
        logging.info(f"✅ Xpath:{self.xpath}, set_text('{value}').")

    def get_text(self):
        """
        get text from field
        :return
        """
        text = self.driver.xpath(self.xpath).get_text()
        logging.info(f"✅ Xpath:{self.xpath}, get_text().")
        return text

    def match(self):
        """
        None or matched XPathElement
        :return:
        """
        match = self.driver.xpath(self.xpath).match()
        logging.info(f"✅ Xpath:{self.xpath}, match().")
        return match


class Element:
    """
    element class
    """

    def __init__(self, timeout=10, describe=None, **kwargs):
        self.describe = describe
        self.timeout = timeout
        if not kwargs:
            raise ValueError("Please specify a locator")
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST:
            raise KeyError(f"Element positioning of type '{self.k}' is not supported.")

    def __get__(self, instance, owner):
        if instance is None:
            return None
        self.driver = instance.driver
        return self

    def click(self, offset=None):
        """
        Click UI element.

        The click method does the same logic as java uiautomator does.
        1. waitForExists 2. get VisibleBounds center 3. send click event

        :raises:
            UiObjectNotFoundError
        :param offset: (xoff, yoff) default (0.5, 0.5) -> center
        :return:
        """
        logging.info(f"✅ click().")
        self.driver(**self.kwargs).click(self.timeout, offset)

    def click_exists(self) -> bool:
        """
        The element is not clicked until it exists
        """
        is_exists = self.driver(**self.kwargs).click_exists(timeout=self.timeout)
        logging.info(f"✅ click_exists().")
        return is_exists

    def click_more(self, sleep: float = .01, times: int = 3):
        """
        Multiple clicks
        sleep:
        times:
        """
        logging.info(f"✅ click_more(times={times}).")
        x, y = self.center()
        for i in range(times):
            self.driver.touch.down(x, y)
            time.sleep(sleep)
            self.driver.touch.up(x, y)

    def exists(self):
        """
        check if the object exists in current window.
        """
        logging.info(f"✅ exists().")
        is_exists = self.driver(**self.kwargs).exists(timeout=self.timeout)
        return is_exists

    def set_text(self, text: str):
        """
        input text
        :param text:
        """
        logging.info(f"⌨️ set text: {text}.")
        self.driver(**self.kwargs).set_text(text=text)

    def send_keys(self, text: str, clear=True):
        """
        alias of set_text
        :param text:
        :param clear:
        """
        logging.info(f"⌨️ send key: {text}.")
        self.driver(**self.kwargs).click()
        self.driver.send_keys(text=text, clear=clear)

    def clear_text(self):
        """
        Clear the text
        """
        logging.info(f"🧹 clear text.")
        self.driver(**self.kwargs).clear()

    def get_text(self):
        """
        get element text
        """
        text = self.driver(**self.kwargs).get_text()
        logging.info(f"✅ get text: {text}.")
        return text

    def bounds(self):
        """
        Returns the element coordinate position
        :return: left_top_x, left_top_y, right_bottom_x, right_bottom_y
        """
        logging.info(f"✅ bounds().")
        return self.driver(**self.kwargs).bounds()

    def get_position(self):
        """
        get position
        :return: x, y
        """
        logging.info(f"✅ get_position().")
        h, w = self.driver.window_size()
        x, y = self.center()
        return round(x / h, 4), round(y / w, 4)

    def center(self):
        """
        Returns the center coordinates of the element
        return: center point (x, y)
        """
        logging.info(f"✅ center().")
        return self.driver(**self.kwargs).center()

    def swipe(self, direction, times=1, steps=10):
        """
        Performs the swipe action on the UiObject.
        Swipe from center

        :param direction: "left", "right", "up", "down"
        :param times: move times
        :param steps: 1 step is about 5ms, if set, duration will be ignored
        :return:
        """
        assert direction in ("left", "right", "up", "down")
        logging.info(f"👆 {direction} swipe, times: {times}.")
        for i in range(times):
            self.driver(**self.kwargs).swipe(direction=direction, steps=steps)
        time.sleep(0.1)

    def sliding(self, height: float = 0.5):
        """
        Determine if the element is on the current page, and if it isn't, slide down until you find it on the screen
            If present, slide the expected position
        :param height: The screen height 0 ~ 1
        :return:
        """
        logging.info(f"👆 sliding found, height: {height}")
        for i in range(30):
            if self.exists():
                break
            else:
                self.driver.swipe(0.5, 0.7, 0.5, 0.3)
        if height:
            if height <= 0 or height >= 1:
                raise ValueError("'h' checks the range of values, 0 < h < 1")
            else:
                scope = [height - 0.05, height + 0.05]
                for i in range(30):
                    x, y = self.get_position()
                    if scope[0] <= y <= scope[1]:
                        break
                    else:
                        if y > scope[1]:
                            self.driver.swipe(0.5, 0.5, 0.5, 0.45)
                        elif y < scope[0]:
                            self.driver.swipe(0.5, 0.45, 0.5, 0.5)

    @property
    def info(self):
        """
        The element information
        """
        info = self.driver(**self.kwargs).info
        logging.info(f"✅ element info: {info}.")
        return info

    @property
    def count(self):
        """
        Gets the same number of elements
        """
        count = self.driver(**self.kwargs).count
        logging.info(f"✅ count().")
        return count

    def instance(self, num: int = 0):
        """
        Click on the list of elements
        """
        _list = []
        self.wait()
        data = self.count
        for i in range(data):
            _list.append(i)
        element = Element(**self.kwargs, instance=_list[num])
        logging.info(f"✅ click {num} element.")
        return element

    def wait(self):
        """
        Wait until UI Element exists or gone
        """
        logging.info(f"🕣 wait {self.timeout}s.")
        return self.driver(**self.kwargs).wait(exists=True, timeout=self.timeout)

    def wait_gone(self):
        """
        wait until ui gone
        :return:
        """
        logging.info(f"🕣 wait {self.timeout}s gone.")
        return self.driver(**self.kwargs).wait_gone(self.timeout)
