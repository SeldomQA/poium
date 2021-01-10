import time
from poium.common import logging
from poium.settings import Setting
from poium.processing import processing, screenshots_name
from poium.common.assert_des import insert_assert


LOCATOR_LIST = [
    "id",
    "name",
    "text",
    "nameContains",
    "label",
    "xpath",
    "labelContains",
    "className",
    "predicate",
    "classChain"
]


class Page(object):

    def __init__(self, dr):
        self.driver = dr

    def native_resolution(self):
        """
        获取屏幕原始分辨率
        """
        multiple = self.driver.scale
        w, h = self.driver.window_size()
        return multiple * w, multiple * h

    @staticmethod
    def wait(sleep=2):
        """
        休眠时间
        """
        time.sleep(sleep)

    def close(self):
        """
        关闭App
        """
        self.driver.close()

    def click(self, x: float=None, y: float=None, text: str=None, screenshots=Setting.click_screenshots):
        """
        点击坐标
        Args：
            x(float): x坐标
            y(float): y坐标
            text(str): 文本
            screenshots(bool): 当screenshots等于True， 会先截图再点击坐标；默认关闭
        """
        if not x and not y and not text:
            raise ValueError
        (x, y) = self.get_position(text=text) if text else (x, y)
        self.screenshots(x, y, describe="点击坐标, {},{}".format(x, y)) if screenshots else \
            (print("\n"), logging.info(msg=" 点击 ==> " + "点击坐标{},{}".format(x, y)))
        self.driver.click(x, y)

    def get_position(self, text=None, element=None):
        """
        获取元素或文本坐标

        Args:
            text(str): 文案
            element(object): atx原生的元素对象
        """
        w, h = self.driver.window_size()
        if text is not None:
            rect = self.driver(name=text).bounds
        elif element is not None:
            rect = element.bounds
        else:
            raise NameError
        x = rect.x + rect.width / 2
        y = rect.y + rect.height / 2
        return x / w, y / h

    def swipe(self, fx: float, fy: float, tx: float, ty: float, duration=0, screenshots=True):
        """
        滑动
        Args:
            fx(float): 起始横坐标
            fy(float): 起始纵坐标
            tx(float): 终点横坐标
            ty(float): 终点纵坐标
            duration(float): 滑动过程的时间 (seconds)
            screenshots(bool): 滑动后截图开关
        """
        self.driver.swipe(fx, fy, tx, ty, duration=duration)
        if screenshots is True:
            time.sleep(0.5)
            self.screenshots()

    def swipe_left(self, fx=0.3, fy=0.5, tx=0.7, ty=0.5, times=1, duration=0, screenshots=True):
        """
        滑向左边
        Args:
            fx(float): 起始横坐标
            fy(float): 起始纵坐标
            tx(float): 终点横坐标
            ty(float): 终点纵坐标
            times(int): 滑动的次数
            duration(float): 滑动过程的时间 (seconds)
            screenshots(bool): 滑动后截图开关
        """
        for i in range(times):
            self.swipe(fx, fy, tx, ty, duration=duration, screenshots=screenshots)

    def swipe_right(self, fx=0.7, fy=0.5, tx=0.3, ty=0.5, times=1, duration=0, screenshots=True):
        """
        滑向右边
        Args:
            fx(float): 起始横坐标
            fy(float): 起始纵坐标
            tx(float): 终点横坐标
            ty(float): 终点纵坐标
            times(int): 滑动的次数
            duration(float): 滑动过程的时间 (seconds)
            screenshots(bool): 滑动后截图开关
        """
        for i in range(times):
            self.swipe(fx, fy, tx, ty, duration=duration, screenshots=screenshots)

    def swipe_up(self, fx=0.5, fy=0.5, tx=0.5, ty=0.8, times=1, duration=0, screenshots=True):
        """
        滑向上边
        Args:
            fx(float): 起始横坐标
            fy(float): 起始纵坐标
            tx(float): 终点横坐标
            ty(float): 终点纵坐标
            times(int): 滑动的次数
            duration(float): 滑动过程的时间 (seconds)
            screenshots(bool): 滑动后截图开关
        """
        for i in range(times):
            self.swipe(fx, fy, tx, ty, duration=duration, screenshots=screenshots)

    def swipe_down(self, fx=0.5, fy=0.5, tx=0.5, ty=0.2, times=1, duration=0, screenshots=True):
        """
        滑向下边
        Args:
            fx(float): 起始横坐标
            fy(float): 起始纵坐标
            tx(float): 终点横坐标
            ty(float): 终点纵坐标
            times(int): 滑动的次数
            duration(float): 滑动过程的时间 (seconds)
            screenshots(bool): 滑动后截图开关
        """
        for i in range(times):
            self.swipe(fx, fy, tx, ty, duration=duration, screenshots=screenshots)

    def swipe_search(self, text, direction="down"):
        """
        文本搜索(不基于元素对象)

        Args:
            text(str): 搜索的内容
            direction(str): "down" 或 "up"
        """
        for i in range(20):
            if self.driver(text=text).exists and self.driver(text=text).displayed:
                break
            else:
                if direction is "down":
                    self.swipe_down()
                elif direction is "up":
                    self.swipe_up()
                else:
                    raise NameError
        else:
            raise TimeoutError("Timeout, element not found")

    def screenshots(self, w=None, h=None, describe=None):
        """
        截图
        """
        if w is not None and h is not None:
            if float(w) < 1 and float(h) < 1:
                multiple = self.driver.scale
                w, h = multiple * w, multiple * h

        screenshots_dir = screenshots_name(describe)
        self.driver.screenshot().save(screenshots_dir)
        processing(screenshots_dir, w, h)

    def who_exists(self, element=None, text=None):
        """
        判断不同页面的多个元素或文本，看哪一个先出现，判断页面的状态
        Args：
            element(list): 元素列表，不同页面的元素对象
            text(list): 文本列表，不同页面的文本
        Return:
            element_child(object): 返回当前页面存在的元素
            text_child(text): 返回当前页面存在的文本
        """
        for i in range(10):
            if element is not None:
                if type(element) is list:
                    for element_child in element:
                        if element_child.exists() is True:
                            return element_child
                else:
                    raise TypeError("The element must be a list")
            elif text is not None:
                if type(text) is list:
                    for text_child in text:
                        if self.driver(nama=text_child).exists is True:
                            return text_child
                else:
                    raise TypeError("The text must be a list")
            else:
                raise ValueError("Must pass parameter")

            time.sleep(1)

        else:
            raise TypeError("The text or element is not exists")

    def alert(self, click=None, timeout=5) -> bool:
        for i in range(timeout):
            if "error" not in self.driver.alert.buttons():
                _list = self.driver.alert.buttons()
                text = self.driver.alert.text
                logging.info(msg="弹窗，提示⚠{text}，选项按钮{button}".format(text=text, button=_list))
                if click == "first":
                    position = self.get_position(text=_list[0])
                    self.screenshots(position[0], position[1])
                    logging.info(msg="👆 ==> {}".format(_list[0]))
                    self.driver.alert.accept()
                elif click == "second":
                    position = self.get_position(text=_list[1])
                    self.screenshots(position[0], position[1])
                    logging.info(msg="👆 ==> {}".format(_list[1]))
                    self.driver.alert.dismiss()
                else:
                    position = self.get_position(text=click)
                    self.screenshots(position[0], position[1])
                    logging.info(msg="👆 ==> {}".format(click))
                    self.driver.alert.click(click)
                return True
            else:
                time.sleep(1)
                continue
        else:
            return False

    def assert_text_exists(self, text: str, describe, sleep=0, timeout=10):
        """
        Asserts that the text exists on the current page

        Args：
            sleep(int): sleep time
            text(str): text
            describe(str): Assertion description information
            timeout(int): Maximum waiting time
        """
        time.sleep(sleep)
        logging.info("预期结果: " + describe + " 文案存在")
        for i in range(timeout):
            text_exists = self.driver(text=text).exists
            if text_exists is True:
                insert_assert(describe, True)
                logging.info("实际结果: " + describe + " 文案存在")
                break
            else:
                time.sleep(1)
                continue
        else:
            insert_assert(describe, False)
            logging.warn("实际结果: " + describe + " 文案不存在")
        self.screenshots(describe="断言")

    def assert_text_contains(self, text: str, describe, sleep=0, timeout=10):
        """
        Asserts that the text exists on the current page

        Args：
            sleep(int): sleep time
            text(str): text
            describe(str): Assertion description information
            timeout(int): Maximum waiting time
        """
        time.sleep(sleep)
        logging.info("预期结果: " + describe + " 文案存在")
        for i in range(timeout):
            text_exists = self.driver(nameContains=text).exists
            if text_exists is True:
                insert_assert(describe, True)
                logging.info("实际结果: " + describe + " 文案存在")
                break
            else:
                time.sleep(1)
                continue
        else:
            insert_assert(describe, False)
            logging.warn("实际结果: " + describe + " 文案不存在")
        self.screenshots(describe="断言")

    def assert_element_exists(self, element, describe, sleep=0, timeout=10):
        """
        Asserts that the text exists on the current page

        Args：
            sleep(int): sleep time
            element: element
            describe(str): Assertion description information
            timeout(int): Maximum waiting time
        """
        time.sleep(sleep)
        logging.info("预期结果: " + describe + " 元素存在")
        for i in range(timeout):
            element_exists = element.exists()
            if element_exists is True:
                insert_assert(describe, True)
                logging.info("实际结果: " + describe + " 元素存在")
                break
            else:
                time.sleep(1)
                continue
        else:
            insert_assert(describe, False)
            logging.warn("实际结果: " + describe + " 元素不存在")
        self.screenshots(describe="断言")

    def assert_text_not_exists(self, text: str, describe, sleep=0, timeout=10):
        """
        Asserts that the text exists on the current page

        Args：
            sleep(int): sleep time
            text(str): text
            describe(str): Assertion description information
            timeout(int): Maximum waiting time
        """
        time.sleep(sleep)
        logging.info("预期结果: " + describe + " 文案不存在")
        for i in range(timeout):
            text_exists = self.driver(text=text).exists
            if text_exists is True:
                insert_assert(describe, False)
                logging.warn("实际结果: " + describe + " 文案存在")
                break
            else:
                time.sleep(1)
                continue
        else:
            insert_assert(describe, True)
            logging.info("实际结果: " + describe + " 文案不存在")
        self.screenshots(describe="断言")

    def assert_element_not_exists(self, element, describe, sleep=0, timeout=10):
        """
        Asserts that the text exists on the current page

        Args：
            sleep(int): sleep time
            element: element
            describe(str): Assertion description information
            timeout(int): Maximum waiting time
        """
        time.sleep(sleep)
        logging.info("预期结果: " + describe + " 元素不存在")
        for i in range(timeout):
            element_exists = element.exists()
            if element_exists is True:
                insert_assert(describe, False)
                logging.warn("实际结果: " + describe + " 元素存在")
                break
            else:
                time.sleep(1)
                continue
        else:
            insert_assert(describe, True)
            logging.info("实际结果: " + describe + " 元素不存在")
        self.screenshots(describe="断言")

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
            logging.info("预期结果: " + text_1 + "," + text_2 + " 相等")
        else:
            result = [describe, False]
            Setting.assert_result.append(result)
            logging.warn("预期结果: " + text_1 + "," + text_2 + " 不相等")

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


class Element(object):

    driver = None

    def __init__(self, timeout=10, describe=None, **kwargs):
        self.time_out = timeout
        self.describe = describe
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

    def click(self, focus=None, beyond=None, screenshots=Setting.click_screenshots):

        """
        点击元素, 根据坐标去点击
        Args:
            focus(list): 点击元素区域的位置，默认点击元素的中心
            beyond(list): 以传的元素为基准，点击相该元素以外的其他位置
            screenshots(bool): 当screenshots等于True， 会先截图再点击坐标；默认关闭
        """
        global driver

        # 通过坐标点击
        w, h = driver.window_size()
        if self.k == "focus":
            if type(self.v) is not list:
                raise ValueError("The argument must be a list")
            elif self.v[0] > 1 or self.v[1] > 1:
                raise ValueError
            x, y = self.v[0] * w, self.v[1] * h
            self.screenshots(x, y, describe="点击, {}".format(self.describe)) if screenshots else \
                (print("\n"), logging.info(msg=" 点击 ==> " + self.describe))
            driver.click(self.v[0], self.v[1])
        else:
            if focus is not None:
                x, y = self.focus(focus)
            elif beyond is not None:
                xx, yy = self.get_position(percentage=False)
                x, y = xx + beyond[0] * w, yy + beyond[1] * h
            else:
                x, y = self.focus([0.5, 0.5])

                self.screenshots(x, y, describe="点击, {}".format(self.describe)) if screenshots else \
                    (print("\n"), logging.info(msg=" 点击 ==> " + self.describe))
            driver.click(x / w, y / h)

    def click_exists(self, timeout=0):
        """
        元素存在，点击元素，不存在就pass
        Args:
            timeout(int): 最大等待时间
        """
        global driver

        return driver(**self.kwargs).click_exists(timeout)

    def wait(self, timeout=10):
        """
        等待元素出现

        Args：
            timeout(int)：等待时间
        """
        global driver
        time.sleep(1)
        driver(**self.kwargs).wait(timeout=timeout)

    def get(self, timeout=10, raise_error=False):
        """
        Args:
            timeout (float): timeout for query element, unit seconds
                Default 10s
            raise_error (bool): whether to raise error if element not found

        Returns:
            Element: UI Element

        Raises:
            WDAElementNotFoundError if raise_error is True else None
        """
        global driver
        driver(**self.kwargs).get(timeout=timeout, raise_error=raise_error)

    def wait_gone(self, timeout=10):
        """
        等待元素消失

        Args：
            timeout(int)：等待时间
        """
        global driver
        driver(**self.kwargs).wait_gone(timeout=timeout)

    def find_elements(self, text=False):
        """
        查找元素

        Args：
            text(bool): 返回元素对应的文本内容
        """
        global driver
        text_list = []
        data = driver(**self.kwargs).find_elements()
        logging.info("查找到匹配数量有==> {}个".format(len(data)))
        if text is True:
            for text_data in data:
                text_list.append(text_data.get_text())
            return text_list
        else:
            return data

    def instance(self, num=1):
        """
        Click on the list of elements
        """
        _list = []
        self.wait()
        data = len(self.find_elements())
        for i in range(data):
            _list.append(i)
        if self.k == "xpath":
            self.kwargs = {"xpath": self.v + "[{}]".format(_list[num] + 1)}
            element = PageElement(**self.kwargs)
        else:
            element = PageElement(**self.kwargs, index=_list[num] + 1)
        return element

    def clear_text(self):
        """
        清空输入框
        """
        global driver
        driver(**self.kwargs).clear_text()

    def set_text(self, text):
        """
        输入文本内容
        Args:
            text(str): 输入栏输入的文本
        """
        global driver
        text = str(text)
        self.clear_text()
        logging.info(msg=" 键盘输入 ==> " + text)
        driver(**self.kwargs).set_text(text)

    def get_text(self):
        """
        获取元素对应的文本
        """
        global driver
        return driver(**self.kwargs).text

    def swipe(self, direction, times=1, distance=1.0):
        """
        基于元素滑动

        times(int): 滑动次数
        distance(float): 滑动距离
        """
        global driver
        assert direction in ("left", "right", "up", "down")

        for i in range(times):
            driver(**self.kwargs).scroll(direction=direction, distance=distance)
        time.sleep(1)

    def focus(self, position):
        """
        定位元素区域内的坐标
        Args:
            position(list): 元素板块内的坐标
        """
        global driver
        self.get()
        if type(position) is not list:
            raise NameError("The argument must be a list")
        elif position[0] > 1 or position[1] > 1:
            raise NameError("Coordinates range from 0 to 1")
        rect = driver(**self.kwargs).bounds
        x = rect.x + rect.width * position[0]
        y = rect.y + rect.height * position[1]
        return x, y

    def get_position(self, percentage=True):
        """
        获取元素坐标
        Args:
            percentage(bool): percentage等于True,坐标是百分比； 默认是真实坐标
        """
        global driver
        self.get()
        w, h = driver.window_size()
        rect = driver(**self.kwargs).bounds
        x = rect.x + rect.width / 2
        y = rect.y + rect.height / 2
        if percentage is True:
            return round(x / w, 6), round(y / h, 6)
        elif percentage is False:
            return x, y

    def exists(self):
        """
        判断元素是否存在
        """
        global driver
        if "index" in self.kwargs:
            return True if len(self.find_elements()) > 0 else False
        else:
            return True if driver(**self.kwargs).exists and driver(**self.kwargs).displayed else False

    def scroll(self, direction='visible', distance=1.0):
        """
        滚动定位到对应的元素
        Args:
            direction (str): one of "visible", "up", "down", "left", "right"
            distance (float): swipe distance, only works when direction is not "visible"

        Raises:
            ValueError

        distance=1.0 means, element (width or height) multiply 1.0
        """
        global driver
        driver(**self.kwargs).scroll(direction=direction, distance=distance)

    def scroll_search(self, click=False, direction="down"):
        """
        滚动定位到对应的元素

        Args:
            click(bool): 定位到元素后，是否点击
            direction(str): 滑动的方向，只能是'down' 或 'or'
        """
        global driver
        for i in range(20):
            if self.exists() is True:
                break
            else:
                if direction is "down":
                    driver.swipe(0.5, 0.5, 0.5, 0.4)
                elif direction is "up":
                    driver.swipe(0.5, 0.5, 0.5, 0.6)
                else:
                    raise ValueError("The direction parameter can only be 'down' or 'up'")
        if click is True:
            self.click(screenshots=True)

    @staticmethod
    def screenshots(w=None, h=None, describe=None):
        """
        截图
        """
        global driver
        screenshots_dir = screenshots_name(describe)
        driver.screenshot().save(screenshots_dir)
        multiple = driver.scale
        w, h = multiple * w, multiple * h
        processing(screenshots_dir, w, h)

    def tap_hold(self, duration=1.0):
        """
        长按

        Args:
            duration (float): seconds of hold time
        """
        global driver
        driver(**self.kwargs).tap_hold(duration=duration)

    def sliding(self, height=0.5, click=False, direction="down"):
        """
        将元素滑动到想要的位置
        Args:
            height(float): 预期将元素滑动到的位置， 位置的范围是 0 ~ 1， 默认是中间
            click(bool): 当click等于True，把元素滑动到预期的位置后，进行点击操作； 默认不点击，只滑动到预期的位置
            direction(str): 滑动的方向，只能是'down' 或 'or'
        """
        if 0 < height < 1:
            height = height
            height_max = height + 0.05
            height_min = height - 0.05
            if direction is "down":
                self.scroll_search(direction="down")
            elif direction is "up":
                self.scroll_search(direction="up")
            else:
                raise ValueError("The direction parameter can only be 'down' or 'up'")
            x, y = self.get_position()
            for i in range(20):
                if height_min <= y <= height_max:
                    break
                move_y = height - y
                if move_y > 0:
                    if move_y >= 0.26:
                        driver.swipe(0.5, 0.5, 0.5, 0.6)
                    elif move_y < 0.26:
                        driver.swipe(0.5, 0.5, 0.5, 0.52, duration=0.5)
                elif move_y < 0:
                    if move_y <= -0.26:
                        driver.swipe(0.5, 0.5, 0.5, 0.4)
                    elif move_y < 0.26:
                        driver.swipe(0.5, 0.5, 0.5, 0.48, duration=0.5)
                x, y = self.get_position()
            time.sleep(1)
            if click is True:
                self.click(screenshots=True)
        else:
            raise ValueError
