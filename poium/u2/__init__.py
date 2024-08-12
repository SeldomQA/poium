from typing import Union

from poium.common import logging
from poium.config import App
from poium.openatx import BasePage

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
        logging.info(f"👆 {orientation} swipe: {fx}, {fy} =>  {tx}, {ty}, times: {times} ")
        for _ in range(times):
            self.driver.swipe(fx, fy, tx, ty, duration, steps)
            self.sleep(1)

    def swipe_down(self, fx=0.5, fy=0.2, tx=0.5, ty=0.8, duration=0.1, times=1):
        """
        swipe down
        :param fx:
        :param fy:
        :param tx:
        :param ty:
        :param duration:
        :param times:
        :return:
        """
        self.swipe(fx, fy, tx, ty, duration=duration, times=times, orientation="down")

    def swipe_up(self, fx=0.5, fy=0.8, tx=0.5, ty=0.2, duration=0, times=1):
        """
        swipe up
        :param fx:
        :param fy:
        :param tx:
        :param ty:
        :param duration:
        :param times:
        :return:
        """
        self.swipe(fx, fy, tx, ty, duration=duration, times=times, orientation="up")

    def swipe_left(self, fx=0.8, fy=0.5, tx=0.2, ty=0.5, duration=0, times=1):
        """
        swipe left
        :param fx:
        :param fy:
        :param tx:
        :param ty:
        :param duration:
        :param times:
        :return:
        """
        self.swipe(fx, fy, tx, ty, duration=duration, times=times, orientation="left")

    def swipe_right(self, fx=0.2, fy=0.5, tx=0.8, ty=0.5, duration=0.1, times=1):
        """
        swipe right
        :param fx:
        :param fy:
        :param tx:
        :param ty:
        :param duration:
        :param times:
        :return:
        """
        self.swipe(fx, fy, tx, ty, duration=duration, times=times, orientation="right")

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

    def __init__(self, xpath, index=None, timeout=10, describe=None):
        self.xpath = xpath
        self.describe = describe
        self.time_out = timeout
        if index is None:
            self.index = 0
        else:
            self.index = int(index)
        self.desc = describe

    def __get__(self, instance, owner):
        if instance is None:
            return None
        App.driver = instance.driver
        return self

    def click(self):
        """
        Click element.
        """
        App.driver.xpath(self.xpath).click()

    def set_text(self, value):
        """
        Simulates typing into the element.
        :param value: input text
        """
        App.driver.xpath(self.xpath).set_text(value)

    def get_text(self):
        """
        :return: get text from field
        """
        return App.driver.xpath(self.xpath).get_text()

    def match(self):
        """
        :return: None or matched XPathElement
        """
        return App.driver.xpath(self.xpath).match()


class Element:
    """
    element class
    """

    def __init__(self, timeout=10, describe=None, **kwargs):
        self.describe = describe
        self.time_out = timeout
        if self.describe is None:
            self.describe = "NONE"
        if not kwargs:
            raise ValueError("Please specify a locator")
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST:
            raise KeyError("Element positioning of type '{}' is not supported.".format(self.k))

    def __get__(self, instance, owner):
        if instance is None:
            return None
        App.driver = instance.driver
        return self

    def click(self, timeout=10, offset=None):
        """
        Click UI element.

        Args:
            timeout: seconds wait element show up
            offset: (xoff, yoff) default (0.5, 0.5) -> center

        The click method does the same logic as java uiautomator does.
        1. waitForExists 2. get VisibleBounds center 3. send click event

        Raises:
            UiObjectNotFoundError
        """
        App.driver(**self.kwargs).click(timeout, offset)

    def click_exists(self, timeout=1):
        """
        The element is not clicked until it exists
        """
        return App.driver(**self.kwargs).click_exists(timeout=timeout)

    def click_more(self, sleep=.01, times=3):
        """
        连续点击
        sleep(float): 间隔时间
        times(int): 点击次数
        """
        x, y = self.center()
        for i in range(times):
            App.driver.touch.down(x, y)
            self.sleep(sleep)
            App.driver.touch.up(x, y)

    def exists(self, timeout=0):
        """
        check if the object exists in current window.
        """

        return App.driver(**self.kwargs).exists(timeout=timeout)

    def set_text(self, text):
        """
        input text
        :param text:
        """
        print("\n")
        logging.info(msg=" 键盘输入 ==> " + text)
        App.driver(**self.kwargs).set_text(text=text)

    def send_keys(self, text, clear=True):
        """
        alias of set_text
        :param text:
        :param clear:
        """
        App.driver(**self.kwargs).click()
        App.driver.send_keys(text=text, clear=clear)

    def clear_text(self):
        """
        Clear the text
        """
        App.driver(**self.kwargs).clear()

    def get_text(self):
        """
        get element text
        """
        return App.driver(**self.kwargs).get_text()

    def bounds(self):
        """
        Returns the element coordinate position
        :return: left_top_x, left_top_y, right_bottom_x, right_bottom_y
        """
        return App.driver(**self.kwargs).bounds()

    def get_position(self):
        """
        get position
        :return: x, y
        """
        h, w = App.driver.window_size()
        x, y = self.center()
        return round(x / h, 4), round(y / w, 4)

    def center(self):
        """
        Returns the center coordinates of the element
        return: center point (x, y)
        """
        return App.driver(**self.kwargs).center()

    def swipe(self, direction, times=1, steps=10):
        """
        Performs the swipe action on the UiObject.
        Swipe from center
        Args:
        steps: 1 steps is about 5ms, if set, duration will be ignore
        direction: "left", "right", "up", "down"
        times: move times
        """
        assert direction in ("left", "right", "up", "down")

        for i in range(times):
            App.driver(**self.kwargs).swipe(direction=direction, steps=steps)
        self.sleep(0.1)

    def sliding(self, h: float = None, click=False):
        """
        Args:
            h(float): The screen height 0 ~ 1
            click(bool): True click the element, False skip
        Documents:
            Determine if the element is on the current page, and if it isn't, slide down until you find it on the screen
            If present, slide the expected position
        """
        for i in range(30):
            if self.exists():
                break
            else:
                App.driver.swipe(0.5, 0.7, 0.5, 0.3)
        if h:
            if h <= 0 or h >= 1:
                raise ValueError("'h' checks the range of values, 0 < h < 1")
            else:
                scope = [h - 0.05, h + 0.05]
                for i in range(30):
                    x, y = self.get_position()
                    if scope[0] <= y <= scope[1]:
                        break
                    else:
                        if y > scope[1]:
                            App.driver.swipe(0.5, 0.5, 0.5, 0.45)
                        elif y < scope[0]:
                            App.driver.swipe(0.5, 0.45, 0.5, 0.5)

        self.click() if click else None

    @property
    def info(self):
        """
        The element information
        """
        return App.driver(**self.kwargs).info

    @property
    def count(self):
        """
        Gets the same number of elements
        """
        return App.driver(**self.kwargs).count

    def instance(self, num):
        """
        Click on the list of elements
        """
        _list = []
        self.wait()
        data = self.count
        for i in range(data):
            _list.append(i)
        element = Element(**self.kwargs, instance=_list[num])
        return element

    def wait(self, timeout=10):
        """
        Wait until UI Element exists or gone
        """
        return App.driver(**self.kwargs).wait(exists=True, timeout=timeout)

    def wait_gone(self, timeout=None):
        """ wait until ui gone
        Args:
            timeout (float): wait element gone timeout
        Returns:
            bool if element gone
        """
        return App.driver(**self.kwargs).wait_gone(timeout)
