import os
import time
from poium.settings import Setting
from poium.common import logging
from poium.processing import processing, screenshots_name
from poium.common.assert_des import insert_assert


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
    "xpath",
]

current_path = os.path.abspath(__file__)
BASE_DIR = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")


class Page(object):

    def __init__(self, dr):
        self.driver = dr

    @staticmethod
    def wait(sleep=1):
        """
        Sleep time
        """
        time.sleep(sleep)

    def window_size(self):
        """
        Documents:
            Resolution size

        Return:
            return (width, height)
        """
        return self.driver.window_size()

    def app_list(self):
        """
        Returns:
            list of apps by filter
        """
        return self.driver.app_list()

    def app_info(self, pkg_name=Setting.apk_name):
        """
        Get app info

        Args:
            pkg_name (str): package name

        Return example:
            {
                "mainActivity": "com.github.uiautomator.MainActivity",
                "label": "ATX",
                "versionName": "1.1.7",
                "versionCode": 1001007,
                "size":1760809
            }

        Raises:
            UiaError
        """
        return self.driver.app_info(pkg_name)

    def click(self, x: float=None, y: float=None, text: str=None, screenshots=Setting.click_screenshots):
        """
        Args:
            x : width / percentage of width
            y : height / percentage of height
            text: text
            screenshots : screenshots
        Documents:
            click position
        """
        if not x and not y and not text:
            raise ValueError
        (x, y) = self.driver(text=text).center() if text else (x, y)
        self.screenshots(x, y, describe="点击") if screenshots else \
            (print("\n"), logging.info(msg=" 点击 ==> " + "点击坐标{},{}".format(x, y)))

        self.driver.click(x, y)

    def click_more(self, x, y, sleep=.01, times=3):
        """
        连续点击
        x: 横坐标
        y: 纵坐标
        sleep(float): 间隔时间
        times(int): 点击次数
        """
        w, h = self.window_size()
        x, y = (w * x, h * y) if x < 1 and y < 1 else x, y
        for i in range(times):
            self.driver.touch.down(x, y)
            time.sleep(sleep)
            self.driver.touch.up(x, y)

    def swipe(self, fx, fy, tx, ty, duration=0.1, steps=None):
        """
        Args:
            fx: from position
            fy: from position
            tx: to position
            ty: to position
            duration (float): duration
            steps: 1 steps is about 5ms, if set, duration will be ignore

        Documents:
            UiAutoMatTor use steps instead of duration
            As the document say: Each step execution is throttled to 5ms per step.
        """
        self.driver.swipe(fx, fy, tx, ty, duration, steps)

    def swipe_down(self, fx=0.5, fy=0.5, tx=0.5, ty=0.2, duration=0.1, times=1, between=0):
        """
        Args:
            fx: from position
            fy: from position
            tx: to position
            ty: to position
            duration (float): duration
            times (int): Slide number
            between (float): Time interval between
        Documents:
            To the following
        """
        for i in range(times):
            self.swipe(fx, fy, tx, ty, duration=duration, steps=None)
            time.sleep(between)

    def swipe_up(self, fx=0.5, fy=0.5, tx=0.5, ty=0.8, duration=0.1, times=1, between=0):
        """
        Args:
            fx: from position
            fy: from position
            tx: to position
            ty: to position
            duration (float): duration
            times (int): Slide number
            between (float): Time interval between

        Documents:
            To the above
        """
        for i in range(times):
            self.swipe(fx, fy, tx, ty, duration=duration, steps=None)
            time.sleep(between)

    def swipe_left(self,  fx=0.3, fy=0.5, tx=0.7, ty=0.5, duration=0.1, times=1, between=0):
        """
        Args:
            fx: from position
            fy: from position
            tx: to position
            ty: to position
            duration (float): duration
            times (int): Slide number
            between (float): Time interval between


        Documents:
            Slide to the left
        """
        for i in range(times):
            self.swipe(fx, fy, tx, ty, duration=duration, steps=None)
            time.sleep(between)

    def swipe_right(self,  fx=0.7, fy=0.5, tx=0.3, ty=0.5, duration=0.1, times=1, between=0):
        """
        Args:
            fx: from position
            fy: from position
            tx: to position
            ty: to position
            duration (float): duration
            times (int): Slide number
            between (float): Time interval between

        Documents:
            Slide to the left
        """
        for i in range(times):
            self.swipe(fx, fy, tx, ty, duration=duration, steps=None)
            time.sleep(between)

    def swipe_search(self, text, direction="down", x: float=None, y: float=None):
        """
        文本搜索(不基于元素对象)

        Args:
            text(str): 搜索的内容
            direction(str): "down" 或 "up"
            x(float): 横坐标滑动起始点
            y(float): 纵坐标滑动起始点
        """
        x = 0.5 if not x else x
        y = 0.5 if not y else y
        for i in range(20):
            if self.driver(textContains=text).exists:
                break
            else:
                if direction is "down":
                    self.swipe_down(fx=x, fy=y, tx=x, ty=y - 0.2, between=1)
                elif direction is "up":
                    self.swipe_up(fx=x, fy=y, tx=x, ty=y + 0.2, between=1)
                else:
                    raise NameError
        else:
            raise TimeoutError("Timeout, element not found")

    def screenshots(self, w=None, h=None, describe=None):
        """
        截图
        """
        if w and h:
            if w < 1 and h < 1:
                x, y = self.window_size()
                w, h = x * w, y * h

        screenshots_dir = screenshots_name(describe)
        self.driver.screenshot(screenshots_dir)
        processing(screenshots_dir, w, h)

    def press(self, key):
        """
        Documents:
            press key via name or key code. Supported key name includes:
            home, back, left, right, up, down, center, menu, search, enter,
            delete(or del), recent(recent apps), volume_up, volume_down,
            volume_mute, camera, power.
        """
        names = ["home", "back", "left", "right", "up", "down", "center", "menu", "search", "enter", "delete", "recent",
                 "volume_up", "volume_down", "volume_mute", "camera", "power"]
        if key in names:
            self.driver.press(key)
        else:
            raise NameError("Check the input text")

    def assert_text_exists(self, text: str, describe: str, sleep=0, timeout=10):
        """
        Asserts that the text exists on the current page

        Args：
            sleep(int): sleep time
            text(str): text
            describe(str): Assertion description information
            timeout(int): Maximum waiting time
        """
        time.sleep(sleep)

        text_exists = self.driver(text=text).exists(timeout)
        self.screenshots(describe="断言")
        logging.info("预期结果: " + describe + " 文案存在")
        if text_exists is True:
            insert_assert(describe, True)
            logging.info("实际结果: " + describe + " 文案存在")
        else:
            insert_assert(describe, False)
            logging.warn("实际结果: " + describe + " 文案不存在")

    def assert_element_exists(self, element, describe, sleep=0, timeout=10):
        """
        Asserts that the element exists on the current page

        Args：
            sleep(int): sleep time
            element(object): element object
            describe(str): Assertion description information
            timeout(int): Maximum waiting time
        """
        time.sleep(sleep)

        element_exists = element.exists(timeout)
        self.screenshots(describe="断言")
        logging.info("预期结果: " + describe + " 元素存在")
        if element_exists is True:
            insert_assert(describe, True)
            logging.info("实际结果: " + describe + " 元素存在")
        else:
            insert_assert(describe, False)
            logging.warn("实际结果: " + describe + " 元素不存在")

    def assert_text_not_exists(self, text, describe, sleep=0, timeout=10):
        """
        Asserts that the text not exists on the current page

        Args：
            sleep(int): sleep time
            text(str): text
            describe(str): Assertion description information
            timeout(int): Maximum waiting time
        """
        time.sleep(sleep)

        text_exists = self.driver(text=text).exists(timeout)
        self.screenshots(describe="断言")
        logging.info("预期结果: " + describe + " 文案不存在")
        if text_exists is True:
            insert_assert(describe, False)
            logging.warn("实际结果: " + describe + " 文案存在")
        else:
            insert_assert(describe, True)
            logging.info("实际结果: " + describe + " 文案不存在")

    def assert_element_not_exists(self, element, describe, sleep=0, timeout=10):
        """
        Asserts that the element not exists on the current page

        Args：
            sleep(int): sleep time
            element(object): element object
            describe(str): Assertion description information
        """
        time.sleep(sleep)

        element_exists = element.exists(timeout)
        self.screenshots(describe="断言")
        logging.info("预期结果: " + describe + " 元素不存在")
        if element_exists is True:
            insert_assert(describe, False)
            logging.warn("实际结果: " + describe + " 元素存在")
        else:
            insert_assert(describe, True)
            logging.info("实际结果: " + describe + " 元素不存在")

    def assert_contain_text(self, text, describe, sleep=0, timeout=10):
        """
        Asserts that two texts are not equal

        Args：
            sleep(int): sleep time
            text(str): text
            describe(str): Assertion description information
            timeout(int): Maximum waiting time
        """
        time.sleep(sleep)

        text_exists = self.driver(textContains=text).exists(timeout)
        self.screenshots(describe="断言")
        logging.info("预期结果: " + describe + " 文案存在")
        if text_exists is True:
            result = [describe, True]
            Setting.assert_result.append(result)
            logging.info("实际结果: " + describe + " 文案存在")
        else:
            result = [describe, False]
            Setting.assert_result.append(result)
            logging.warn("实际结果: " + describe + " 文案不存在")

    def assert_not_contain_text(self, text, describe, sleep=0, timeout=10):
        """
        Asserts that two texts are not equal

        Args：
            sleep(int): sleep time
            text(str): text
            describe(str): Assertion description information
            timeout(int): Maximum waiting time
        """
        time.sleep(sleep)

        text_exists = self.driver(textContains=text).exists(timeout)
        self.screenshots(describe="断言")
        logging.info("预期结果: " + describe + " 文案不存在")
        if text_exists is True:
            result = [describe, False]
            Setting.assert_result.append(result)
            logging.warn("实际结果: " + describe + " 文案存在")
        else:
            result = [describe, True]
            Setting.assert_result.append(result)
            logging.info("实际结果: " + describe + " 文案不存在")

    @staticmethod
    def assert_text_equals(text_1, text_2, describe):
        """
        Asserts that two texts are equal

        Args：
            text(list): text
        """
        logging.info("预期结果: " + text_1 + "," + text_2 + " 相等")

        if text_1 == text_2:
            result = [describe, True]
            Setting.assert_result.append(result)
            logging.info("实际结果: " + text_1 + "," + text_2 + " 相等")

        else:
            result = [describe, False]
            Setting.assert_result.append(result)
            logging.warn("实际结果: " + text_1 + "," + text_2 + " 不相等")

    @staticmethod
    def assert_text_not_equals(text_1, text_2, describe):
        """
        Asserts that two texts are not equal

        Args：
            text(list): text
        """
        logging.info("预期结果: " + text_1 + "," + text_2 + " 不相等")
        if text_1 == text_2:
            result = [describe, False]
            Setting.assert_result.append(result)
            logging.warn("预期结果: " + text_1 + "," + text_2 + " 相等")
        else:
            result = [describe, True]
            Setting.assert_result.append(result)
            logging.info("预期结果: " + text_1 + "," + text_2 + " 不相等")


class XpathElement(object):
    """
    Only CSS selectors are supported.
    https://github.com/openatx/uiautomator2/blob/master/XPATH.md

    >> from sabre import Page, XpathElement
    >> class MyPage(Page):
            input = XpathElement('//android.widget.EditText')
            button = XpathElement('@com.taobao.taobao:id/fl_banner_container')
    """

    driver = None

    def __init__(self, xpath, index=None, timeout=10, describe=None):
        self.xpath = xpath
        self.describe = describe
        if index is None:
            self.index = 0
        else:
            self.index = int(index)
        self.desc = describe

    def __get__(self, instance, owner):
        if instance is None:
            return None
        global driver
        driver = instance.driver
        return self

    def click(self, screenshots=Setting.click_screenshots):
        """
        Click element.
        """
        self.screenshots(describe="点击") if screenshots else (logging.info(msg="点击 ==> " + self.describe), print("\n"))

        driver.xpath(self.xpath).click()

    def set_text(self, value):
        """
        Simulates typing into the element.
        :param value: input text
        """
        driver.xpath(self.xpath).set_text(value)

    def get_text(self):
        """
        :return: get text from field
        """
        return driver.xpath(self.xpath).get_text()

    def match(self):
        """
        :return: None or matched XPathElement
        """
        return driver.xpath(self.xpath).match()

    def screenshots(self, describe=None):
        """
        截图，在对应元素上增加水印
        """
        global driver
        text = driver.xpath(self.xpath).get_text()
        if text == "":
            w, h = None, None
        else:
            w, h = driver(text=text).center()
        screenshots_dir = screenshots_name(describe)
        driver.screenshot(screenshots_dir)
        processing(screenshots_dir, w, h)


class Element(object):

    driver = None

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
        global driver
        driver = instance.driver
        return self

    def click(self, timeout=10, offset=None, screenshots=Setting.click_screenshots):
        """
        Click UI element.

        Args:
            timeout: seconds wait element show up
            offset: (xoff, yoff) default (0.5, 0.5) -> center
            screenshots: screenshots

        The click method does the same logic as java uiautomator does.
        1. waitForExists 2. get VisibleBounds center 3. send click event

        Raises:
            UiObjectNotFoundError
        """
        global driver
        driver(**self.kwargs).click(timeout, offset)

    def click_exists(self, timeout=1, screenshots=Setting.click_screenshots):
        """
        The element is not clicked until it exists
        """

        global driver
        return driver(**self.kwargs).click_exists(timeout=timeout)

    def click_more(self, sleep=.01, times=3):
        """
        连续点击
        sleep(float): 间隔时间
        times(int): 点击次数
        """
        global driver
        x, y = self.center()
        for i in range(times):
            driver.touch.down(x, y)
            time.sleep(sleep)
            driver.touch.up(x, y)

    def exists(self, timeout=0):
        """
        check if the object exists in current window.
        """

        global driver

        return driver(**self.kwargs).exists(timeout=timeout)

    def set_text(self, text):
        """
        input text
        :param text:
        """
        global driver

        print("\n")
        logging.info(msg=" 键盘输入 ==> " + text)
        driver(**self.kwargs).set_text(text=text)

    def send_keys(self, text, clear=True):
        """
        alias of set_text
        :param text:
        :param clear:
        """
        global driver

        driver(**self.kwargs).click()
        driver.send_keys(text=text, clear=clear)

    def clear_text(self):
        """
        Clear the text
        """
        global driver

        driver(**self.kwargs).clear()

    def get_text(self):
        """
        get element text
        """
        global driver

        return driver(**self.kwargs).get_text()

    def bounds(self):
        """
        Returns the element coordinate position
        :return: left_top_x, left_top_y, right_bottom_x, right_bottom_y
        """
        global driver

        return driver(**self.kwargs).bounds()

    def get_position(self):
        global driver
        h, w = driver.window_size()
        x, y = self.center()
        return round(x / h, 4), round(y / w, 4)

    def center(self):
        """
        Returns the center coordinates of the element
        return: center point (x, y)
        """
        global driver

        return driver(**self.kwargs).center()

    def swipe(self, direction, times=1, steps=10):
        """
        Performs the swipe action on the UiObject.
        Swipe from center
        Args:
        steps: 1 steps is about 5ms, if set, duration will be ignore
        direction: "left", "right", "up", "down"
        times: move times
        """
        global driver
        assert direction in ("left", "right", "up", "down")

        for i in range(times):
            driver(**self.kwargs).swipe(direction=direction, steps=steps)
        time.sleep(1)

    def sliding(self, h: float=None, click=False):
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
                driver.swipe(0.5, 0.7, 0.5, 0.3)
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
                            driver.swipe(0.5, 0.5, 0.5, 0.45)
                        elif y < scope[0]:
                            driver.swipe(0.5, 0.45, 0.5, 0.5)

        self.click() if click else None

    @property
    def info(self):
        """
        The element information
        """
        global driver
        return driver(**self.kwargs).info

    @property
    def count(self):
        """
        Gets the same number of elements
        """
        global driver
        return driver(**self.kwargs).count

    def instance(self, num):
        """
        Click on the list of elements
        """
        _list = []
        time.sleep(1)
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
        global driver
        return driver(**self.kwargs).wait(exists=True, timeout=timeout)

    def wait_gone(self, timeout=None):
        """ wait until ui gone
        Args:
            timeout (float): wait element gone timeout
        Returns:
            bool if element gone
        """
        global driver
        return driver(**self.kwargs).wait_gone(timeout)

    def screenshots(self, describe=None):
        """
        A screenshot that adds a watermark to the corresponding element
        """
        global driver
        w, h = self.center()
        screenshots_dir = screenshots_name(describe)
        driver.screenshot(screenshots_dir)
        processing(screenshots_dir, w, h)
