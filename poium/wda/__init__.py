import time

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
        self.timeout = timeout
        self.describe = describe
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

    def click(self, focus=None, beyond=None):
        """
        click coordinate position element.
        :param focus: Click the location of the element area, the default click is the center of the element
        :param beyond: Based on the passed element, click on a location other than that element
        :return:
        """
        logging.info(f"✅ click().")
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

    def click_exists(self):
        """
        The element is not clicked until it exists
        :return:
        """
        is_exists = self.driver(**self.kwargs).click_exists(self.timeout)
        logging.info(f"✅ click_exists().")
        return is_exists

    def wait(self):
        """
        Wait until UI Element exists
        :return:
        """
        logging.info(f"🕣 wait {self.timeout}s.")
        return self.driver(**self.kwargs).wait(timeout=self.timeout)

    def wait_gone(self):
        """
        wait until ui gone
        :return:
        """
        logging.info(f"🕣 wait {self.timeout}s gone.")
        return self.driver(**self.kwargs).wait_gone(timeout=self.timeout)

    def get(self, raise_error: bool = False):
        """
        Get UI Element
        :param raise_error: whether to raise error if element not found
        :return:
        """
        logging.info(f"✅ get UI element.")
        return self.driver(**self.kwargs).get(timeout=self.timeout, raise_error=raise_error)

    def find_elements(self, text=False):
        """
        查找元素

        Args：
            text(bool): 返回元素对应的文本内容
        """
        logging.info(f"🔍 find elements: {text}.")
        data = self.driver(**self.kwargs).find_elements()
        logging.info(f"I found {len(data)} of them.")

        if text is True:
            text_list = []
            for text_data in data:
                text_list.append(text_data.get_text())
            return text_list
        else:
            return data

    def instance(self, num: int = 0):
        """
        Click on the list of elements
        """
        _list = []
        self.wait()
        data = len(self.find_elements())
        for i in range(data):
            _list.append(i)
        if self.k == "xpath":
            self.kwargs = {"xpath": self.v + "[{}]".format(_list[num])}
            element = Element(**self.kwargs)
        else:
            element = Element(**self.kwargs, index=_list[num])

        logging.info(f"✅ click {num} element.")

        return element

    def set_text(self, text: str):
        """
        input text
        :param text:
        """
        logging.info(f"⌨️ set text: {text}.")
        self.clear_text()
        self.driver(**self.kwargs).set_text(text)

    def clear_text(self):
        """
        Clear the text
        """
        logging.info(f"🧹 clear text.")
        self.driver(**self.kwargs).clear_text()

    def get_text(self):
        """
        获取元素对应的文本
        """
        text = self.driver(**self.kwargs).text
        logging.info(f"✅ get text: {text}.")
        return text

    def swipe(self, direction, times=1, distance=1.0):
        """
        Element-based sliding

        :param direction: "left", "right", "up", "down"
        :param times: move times
        :param distance: 滑动距离
        :return:
        """
        assert direction in ("left", "right", "up", "down")
        logging.info(f"👆 {direction} swipe, times: {times}.")
        for i in range(times):
            self.driver(**self.kwargs).scroll(direction=direction, distance=distance)
        time.sleep(0.1)

    def focus(self, position: list):
        """
        Locate coordinates within the element region
        :param position: Coordinates on the element region
        :return:
        """
        logging.info(f"👆 focus, position: {position}.")
        self.get()
        if type(position) is not list:
            raise NameError("The argument must be a list")
        elif position[0] > 1 or position[1] > 1:
            raise NameError("Coordinates range from 0 to 1")

        rect = self.driver(**self.kwargs).bounds
        x = rect.x + rect.width * position[0]
        y = rect.y + rect.height * position[1]
        return x, y

    def get_position(self, percentage: bool = False):
        """
        Get element coordinates
        :param percentage: True: percentage , False: Default is real coordinates
        :return:
        """

        self.get()
        w, h = self.driver.window_size()
        rect = self.driver(**self.kwargs).bounds
        x = rect.x + rect.width / 2
        y = rect.y + rect.height / 2
        if percentage is True:
            x, y = round(x / w, 6), round(y / h, 6)
        logging.info(f"ℹ️ get element position: [{x}, {y}].")
        return x, y

    def exists(self):
        """
        check if the object exists in current window.
        """
        logging.info(f"✅ exists().")
        if "index" in self.kwargs:
            return True if len(self.find_elements()) > 0 else False
        else:
            return True if self.driver(**self.kwargs).exists and self.driver(**self.kwargs).displayed else False

    def swipe_search(self, direction="up"):
        """
        Scroll to locate the corresponding element
        :param direction: 'down' or 'up'
        :return:
        """
        logging.info(f"🔍 swipe search.")
        for i in range(20):
            if self.exists() is True:
                break
            else:
                if direction == "up":
                    self.driver.swipe(0.5, 0.6, 0.5, 0.4)
                elif direction == "down":
                    self.driver.swipe(0.5, 0.4, 0.5, 0.6)
                else:
                    raise ValueError("The direction parameter can only be 'down' or 'up'")

    def sliding(self, height: float = 0.5):
        """
         Determine if the element is on the current page, and if it isn't, slide down until you find it on the screen
            If present, slide the expected position
        :param height:  The screen height 0 ~ 1
        :return:
        """
        logging.info(f"👆 sliding found, height: {height}")
        if 0 < height < 1:
            height = height
            height_max = height + 0.05
            height_min = height - 0.05
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

        else:
            raise ValueError("height: The screen height 0 ~ 1")
