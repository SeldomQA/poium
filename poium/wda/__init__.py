import time


LOCATOR_LIST = [
    "id",
    "name",
    "text",
    "nameContains",
    "label",
    "xpath",
    "labelContains",
    "className"
]


class Page(object):

    def __init__(self, dr):
        self.driver = dr

    def bundle_id(self):
        """
        the session matched bundle id
        """
        return self.driver.bundle_id

    def locked(self):
        """
        returns locked status, true or false
        """
        return self.driver.locked()

    def lock(self):
        """
        Execute screen lock
        """
        return self.driver.lock()

    def unlock(self):
        """
        unlock screen, double press home
        """
        return self.driver.unlock()

    def battery_info(self):
        """
        Returns dict: (I do not known what it means)
        """
        return self.driver.battery_info()

    def device_info(self):
        """
        Returns dict: (I do not known what it means)
        """
        return self.driver.device_info()

    def app_current(self):
        """
        Current application information
        """
        return self.driver.app_current()

    def set_clipboard(self):
        """
        set clipboard
        """
        self.driver.set_clipboard()

    def window_size(self):
        """
        Gets the real resolution of the screen
        """
        multiple = self.driver.scale
        w, h = self.driver.window_size()
        return multiple * w, multiple * h

    def close(self):
        """
        close App
        """
        self.driver.close()

    def swipe(self, start, end, duration=0):
        """
        滑动
        start:
            list类型，起始坐标
        end:
            list类型，终点坐标
        """
        if type(start) is list or type(end) is list:
            self.driver.swipe(start[0], start[1], end[0], end[1], duration)
        else:
            raise TypeError("The argument must be a list")

    def swipe_left(self, pos, times=None):
        """
        滑向左边
        times:
            int类型， 滑动的次数
        """
        if times is None:
            times = 1
        if type(pos) is list:
            for i in range(times):
                self.swipe([pos[0], pos[1]], [pos[0] + 0.2, pos[1]])
        else:
            raise TypeError("The argument must be a list")

    def swipe_right(self, pos, times=False):
        """
        滑向右边
        times:
            int类型， 滑动的次数
        """
        if times is False:
            times = 1
        if type(pos) is list:
            for i in range(times):
                self.swipe([pos[0], pos[1]], [pos[0] - 0.2, pos[1]])
        else:
            raise TypeError("The argument must be a list")

    def swipe_up(self, times=False):
        """
        向上滑动
        times:
            int类型， 滑动的次数
        """
        if times is False:
            times = 1
        for i in range(times):
            self.swipe([0.5, 0.3], [0.5, 0.6])

    def swipe_down(self, times=False):
        """
        向下滑动
        times:
            int类型， 滑动的次数
        """
        if times is False:
            times = 1
        for i in range(times):
            self.swipe([0.5, 0.6], [0.5, 0.3])


class PageElement(object):

    driver = None

    def __init__(self, timeout=10, describe=None, **kwargs):
        self.time_out = timeout
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

    def click(self):
        """
        点击元素
        """
        global driver
        for i in range(self.time_out):
            time.sleep(1)
            if driver(**self.kwargs).exists:
                break
        else:
            raise NameError("No corresponding element was found")
        driver(**self.kwargs).click()

    def set_text(self, value):
        """
        输入文本内容
         value:
              Must be of type string
        """
        global driver
        if type(value) is str:
            driver(**self.kwargs).set_text(value)

    def get_text(self):
        """
        获取元素对应的文本
        """
        global driver
        return driver(**self.kwargs).text

    def focus(self, position):
        """
        定位元素区域内的坐标
        :return:
        """
        global driver
        if type(position) is not list:
            raise NameError("The argument must be a list")
        elif position[0] > 1 or position[1] > 1:
            raise NameError("Coordinates range from 0 to 1")
        w, h = driver.window_size()
        rect = driver(**self.kwargs).bounds
        x = rect.x + rect.width * position[0]
        y = rect.y + rect.height * position[1]
        return x / w, y / h

    def focus_click(self, position):
        """
        点击元素范围内的某个位置
        :return:
        """
        if type(position) is not list:
            raise NameError("The argument must be a list")
        elif position[0] > 1 or position[1] > 1:
            raise NameError("Coordinates range from 0 to 1")
        x, y = self.focus(position=position)
        driver.click(x, y)

    def get_position(self, percentage=True):
        """
        获取元素坐标
        :return: 返回坐标百分比
        """
        global driver
        w, h = driver.window_size()
        rect = driver(**self.kwargs).bounds
        x = rect.x + rect.width / 2
        y = rect.y + rect.height / 2
        if percentage is True:
            return x / w, y / h
        elif percentage is False:
            return x, y

    def exists(self):
        """
        判断元素是否存在
        """
        global driver
        status = driver(**self.kwargs).exists
        return status

    def displayed(self):
        """
        判断元素是否存当前页面
        """
        global driver
        status = driver(**self.kwargs).displayed
        return status

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

    def scroll_search(self, click=False):
        """
        滚动定位到对应的元素

        Args:
            click: 定位到元素后，是否点击
        """
        global driver
        driver(**self.kwargs).scroll()
        if click is True:
            self.click()

    def swipe(self, direction, times=1):
        """
        基于元素滑动

        Args:
            direction (str): 方向，只能填写'up', 'down', 'left', 'right'
            times (int): 滑动次数
        """
        global driver
        x, y = self.get_position()
        if direction in ['up', 'down', 'left', 'right']:
            for i in range(times):
                if direction is "up":
                    driver.swipe(x, 0.5, x, 0.6)
                elif direction is "down":
                    driver.swipe(x, 0.5, x, 0.4)
                elif direction is "left":
                    driver.swipe(x, y, x + 0.15, y)
                elif direction is "right":
                    driver.swipe(x, y, x - 0.15, y)
        else:
            raise NameError

    def swipe_down(self, times=1):
        """
        基于元素向下滑动

        Args:
            times（int）: 滑动次数
        """
        self.swipe(direction="down", times=times)

    def swipe_up(self, times=1):
        """
        基于元素向上滑动

        Args:
            times（int）: 滑动次数
        """
        self.swipe(direction="up", times=times)

    def swipe_left(self, times=1):
        """
        基于元素向左滑动

        Args:
            times（int）: 滑动次数
        """
        self.swipe(direction="left", times=times)

    def swipe_right(self, times=1):
        """
        基于元素向右滑动

        Args:
            times（int）: 滑动次数
        """
        self.swipe(direction="right", times=times)

    def tap_hold(self, duration=1.0):
        """
        Tap and hold for a moment

        Args:
            duration (float): seconds of hold time
        """
        global driver
        driver(**self.kwargs).tap_hold(duration=duration)

    def precision_move(self, height):
        """
        将元素滑动到想要的位置
        :param height:
        :return:
        """
        if 0 < height < 1:
            x, y = self.get_position()
            height_max = height + 0.05
            height_min = height - 0.05
            for i in range(10):
                if height_min <= y <= height_max:
                    break
                if 0 <= height - y < 0.3:
                    self.scroll(direction="up", distance=1)
                elif height - y >= 0.3:
                    self.swipe_down()
                elif -0.3 < height - y <= 0:
                    self.scroll(direction="down", distance=1)
                elif -0.3 >= height - y:
                    self.swipe_up()
                x, y = self.get_position()
        else:
            raise ValueError
