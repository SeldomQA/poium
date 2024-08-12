from poium.common import logging
from poium.common.openatx import BasePage

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


class Page(BasePage):
    """
    facebook-wda page class
    """

    def native_resolution(self):
        """
        Gets the original screen resolution.
        """
        multiple = self.driver.scale
        w, h = self.driver.window_size()
        return multiple * w, multiple * h

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
        (x, y) = self.get_position(text=text) if text else (x, y)

        logging.info(f"👆 click: {x}, {y}")
        self.driver.click(x, y)

    def get_position(self, text=None, element=None):
        """
        Gets element or text position
        :param text:
        :param element:
        :return:
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

    def swipe(self, fx: float, fy: float, tx: float, ty: float, duration=0, times=1, orientation: str = ""):
        """
        swipe
        :param fx:
        :param fy:
        :param tx:
        :param ty:
        :param duration:
        :param times:
        :param orientation:
        :return:
        """
        logging.info(f"👆 {orientation} swipe: [{fx}, {fy} =>  {tx}, {ty}], times: {times} ")
        for _ in range(times):
            self.driver.swipe(fx, fy, tx, ty, duration=duration)
            self.sleep(1)

    def swipe_search(self, text, direction="up"):
        """
        swipe search text
        :param text:
        :param direction: "down" or "up"
        :return:
        """
        logging.info(f"🔍 swipe search: {text}")
        for i in range(20):
            if self.driver(text=text).exists and self.driver(text=text).displayed:
                break
            else:
                if direction == "down":
                    self.swipe_down()
                elif direction == "up":
                    self.swipe_up()
                else:
                    raise NameError
        else:
            raise TimeoutError("Timeout, element not found")

    def who_exists(self, element: list = None, text: list = None):
        """
            Determine multiple elements or text for different pages,
        see which comes first, and determine the state of the page
        :param element: Element objects for different pages.
        :param text: text for different pages.
        :return:
            element_child(object): Returns the elements that exist on the current page
            text_child(text): Returns the text that exists on the current page
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

            self.sleep(1)

        else:
            raise TypeError("The text or element is not exists")

    def alert(self, click=None, timeout=5) -> bool:
        """
        click error alert.
        :param click:
        :param timeout:
        :return:
        """
        for i in range(timeout):
            if "error" not in self.driver.alert.buttons():
                _list = self.driver.alert.buttons()
                text = self.driver.alert.text
                logging.info(f"alert prompt:⚠ {text}, option button: {_list}")
                if click == "first":
                    logging.info(f"👆 ==> {_list[0]}")
                    self.driver.alert.accept()
                elif click == "second":
                    logging.info(f"👆 ==> {_list[1]}")
                    self.driver.alert.dismiss()
                else:
                    logging.info(f"👆 ==> {click}")
                    self.driver.alert.click(click)
                return True
            else:
                self.sleep(1)
                continue
        else:
            return False


class Element(object):
    """
    element class
    """

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

        self.driver = instance.driver
        return self

    def click(self, focus=None, beyond=None):

        """
        点击元素, 根据坐标去点击
        Args:
            focus(list): 点击元素区域的位置，默认点击元素的中心
            beyond(list): 以传的元素为基准，点击相该元素以外的其他位置
        """

        # 通过坐标点击
        w, h = self.driver.window_size()
        if self.k == "focus":
            if type(self.v) is not list:
                raise ValueError("The argument must be a list")
            elif self.v[0] > 1 or self.v[1] > 1:
                raise ValueError
            self.driver.click(self.v[0], self.v[1])
        else:
            if focus is not None:
                x, y = self.focus(focus)
            elif beyond is not None:
                xx, yy = self.get_position(percentage=False)
                x, y = xx + beyond[0] * w, yy + beyond[1] * h
            else:
                x, y = self.focus([0.5, 0.5])

            self.driver.click(x / w, y / h)

    def click_exists(self, timeout=0):
        """
        元素存在，点击元素，不存在就pass
        Args:
            timeout(int): 最大等待时间
        """

        return self.driver(**self.kwargs).click_exists(timeout)

    def wait(self, timeout=10):
        """
        等待元素出现

        Args：
            timeout(int)：等待时间
        """
        self.driver(**self.kwargs).wait(timeout=timeout)

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
        self.driver(**self.kwargs).get(timeout=timeout, raise_error=raise_error)

    def wait_gone(self, timeout=10):
        """
        等待元素消失

        Args：
            timeout(int)：等待时间
        """
        self.driver(**self.kwargs).wait_gone(timeout=timeout)

    def find_elements(self, text=False):
        """
        查找元素

        Args：
            text(bool): 返回元素对应的文本内容
        """
        text_list = []
        data = self.driver(**self.kwargs).find_elements()
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
            element = Element(**self.kwargs)
        else:
            element = Element(**self.kwargs, index=_list[num] + 1)
        return element

    def clear_text(self):
        """
        清空输入框
        """
        self.driver(**self.kwargs).clear_text()

    def set_text(self, text):
        """
        输入文本内容
        Args:
            text(str): 输入栏输入的文本
        """
        text = str(text)
        self.clear_text()
        logging.info(msg=" 键盘输入 ==> " + text)
        self.driver(**self.kwargs).set_text(text)

    def get_text(self):
        """
        获取元素对应的文本
        """
        return self.driver(**self.kwargs).text

    def swipe(self, direction, times=1, distance=1.0):
        """
        基于元素滑动

        times(int): 滑动次数
        distance(float): 滑动距离
        """
        assert direction in ("left", "right", "up", "down")

        for i in range(times):
            self.driver(**self.kwargs).scroll(direction=direction, distance=distance)

    def focus(self, position):
        """
        定位元素区域内的坐标
        Args:
            position(list): 元素板块内的坐标
        """
        self.get()
        if type(position) is not list:
            raise NameError("The argument must be a list")
        elif position[0] > 1 or position[1] > 1:
            raise NameError("Coordinates range from 0 to 1")
        rect = self.driver(**self.kwargs).bounds
        x = rect.x + rect.width * position[0]
        y = rect.y + rect.height * position[1]
        return x, y

    def get_position(self, percentage=True):
        """
        获取元素坐标
        Args:
            percentage(bool): percentage等于True,坐标是百分比； 默认是真实坐标
        """
        self.get()
        w, h = self.driver.window_size()
        rect = self.driver(**self.kwargs).bounds
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
        if "index" in self.kwargs:
            return True if len(self.find_elements()) > 0 else False
        else:
            return True if self.driver(**self.kwargs).exists and self.driver(**self.kwargs).displayed else False

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
        self.driver(**self.kwargs).scroll(direction=direction, distance=distance)

    def scroll_search(self, click=False, direction="down"):
        """
        滚动定位到对应的元素

        Args:
            click(bool): 定位到元素后，是否点击
            direction(str): 滑动的方向，只能是'down' 或 'or'
        """
        for i in range(20):
            if self.exists() is True:
                break
            else:
                if direction == "down":
                    self.driver.swipe(0.5, 0.5, 0.5, 0.4)
                elif direction == "up":
                    self.driver.swipe(0.5, 0.5, 0.5, 0.6)
                else:
                    raise ValueError("The direction parameter can only be 'down' or 'up'")
        if click is True:
            self.click()

    def tap_hold(self, duration=1.0):
        """
        长按

        Args:
            duration (float): seconds of hold time
        """
        self.driver(**self.kwargs).tap_hold(duration=duration)

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
            if direction == "down":
                self.scroll_search()
            elif direction == "up":
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
                        self.driver.swipe(0.5, 0.5, 0.5, 0.6)
                    elif move_y < 0.26:
                        self.driver.swipe(0.5, 0.5, 0.5, 0.52, duration=0.5)
                elif move_y < 0:
                    if move_y <= -0.26:
                        self.driver.swipe(0.5, 0.5, 0.5, 0.4)
                    elif move_y < 0.26:
                        self.driver.swipe(0.5, 0.5, 0.5, 0.48, duration=0.5)
                x, y = self.get_position()

            if click is True:
                self.click()
        else:
            raise ValueError
