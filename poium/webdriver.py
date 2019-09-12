import os
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from appium.webdriver.common.touch_action import TouchAction as MobileTouchAction

from .page_objects import PageObject


class Page(PageObject):
    """
    Implement the APIs with javascript,
    and selenium/appium extension APIs。
    """

    def window_scroll(self, width=None, height=None):
        """
        JavaScript API, Only support css positioning
        Setting width and height of window scroll bar.
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = "window.scrollTo({w},{h});".format(w=width, h=height)
        self.driver.execute_script(js)

    @property
    def get_title(self):
        """
        JavaScript API
        Get page title.
        """
        js = 'return document.title;'
        return self.driver.execute_script(js)

    @property
    def get_url(self):
        """
        JavaScript API
        Get page URL.
        """
        js = "return document.URL;"
        return self.driver.execute_script(js)

    def switch_to_frame(self, frame_reference):
        """
        selenium API
        Switches focus to the specified frame, by id, name, or webelement.
        """
        self.driver.switch_to.frame(frame_reference)

    def switch_to_parent_frame(self):
        """
        selenium API
        Switches focus to the parent context.
        Corresponding relationship with switch_to_frame () method.
        """
        self.driver.switch_to.parent_frame()

    @property
    def new_window_handle(self):
        """
        selenium API
        Getting a handle to a new window.
        """
        original_window = self.driver.current_window_handle
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != original_window:
                new_handle = handle
                break
        else:
            new_handle = None
        return new_handle

    @property
    def current_window_handle(self):
        """
        selenium API
        Returns the handle of the current window.
        """
        return self.driver.current_window_handle

    @property
    def window_handles(self):
        """
        selenium API
        Returns the handles of all windows within the current session.
        """
        return self.driver.window_handles

    def switch_to_window(self, handle):
        """
        selenium API
        Switches focus to the specified window.
        """
        self.driver.switch_to.window(handle)

    def screenshots(self, path=None, filename=None):
        """
        selenium API
        Saves a screenshots of the current window to a PNG image file
        :param path: The path to save the file
        :param filename: The file name
        """
        if path is None:
            path = os.getcwd()
        if filename is None:
            filename = str(time.time()).split(".")[0] + ".png"
        file_path = os.path.join(path, filename)
        self.driver.save_screenshot(file_path)

    def switch_to_app(self):
        """
        appium API
        Switch to native app.
        """
        self.driver.switch_to.context('NATIVE_APP')

    def switch_to_web(self, context=None):
        """
        appium API
        Switch to web view.
        """
        if context is not None:
            self.driver.switch_to.context(context)
        else:
            all_context = self.driver.contexts
            for context in all_context:
                if "WEBVIEW" in context:
                    self.driver.switch_to.context(context)
                    break
            else:
                raise NameError("No WebView found.")

    def accept_alert(self):
        """
        selenium API
        Accept warning box.
        """
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        selenium API
        Dismisses the alert available.
        """
        self.driver.switch_to.alert.dismiss()

    @property
    def get_alert_text(self):
        """
        selenium API
        Get warning box prompt information.
        """
        return self.driver.switch_to.alert.text

    def move_to_element(self, elem):
        """
        selenium API
        Moving the mouse to the middle of an element
        """
        ActionChains(self.driver).move_to_element(elem).perform()

    def click_and_hold(self, elem):
        """
        selenium API
        Holds down the left mouse button on an element.
        """
        ActionChains(self.driver).click_and_hold(elem).perform()

    def move_by_offset(self, x, y):
        """
        selenium API
        Moving the mouse to an offset from current mouse position.

        :Args:
         - x: X offset to move to, as a positive or negative integer.
         - y: Y offset to move to, as a positive or negative integer.
        """
        ActionChains(self.driver).move_by_offset(x, y).perform()

    def release(self):
        """
        selenium API
        Releasing a held mouse button on an element.
        """
        ActionChains(self.driver).release().perform()

    def context_click(self, elem):
        """
        selenium API
        Performs a context-click (right click) on an element.
        """
        ActionChains(self.driver).context_click(elem).perform()

    def drag_and_drop_by_offset(self, elem, x, y):
        """
        selenium API
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.
        :param elem: The element to mouse down.
        :param x: X offset to move to.
        :param y: Y offset to move to.
        """
        ActionChains(self.driver).drag_and_drop_by_offset(elem, xoffset=x, yoffset=y).perform()

    def refresh_element(self, elem, timeout=10):
        """
        selenium API
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

    def top(self, elem, x, y, count):
        """
        appium API
        Perform a tap action on the element
        """
        action = MobileTouchAction(self.driver)
        action.tap(elem, x, y, count).perform()

    def press(self, elem, x, y, pressure):
        """
        appium API
        Begin a chain with a press down action at a particular element or point
        """
        action = MobileTouchAction(self.driver)
        action.press(elem, x, y, pressure).perform()

    def long_press(self, elem, x, y, duration):
        """
        appium API
        Begin a chain with a press down that lasts `duration` milliseconds
        """
        action = MobileTouchAction(self.driver)
        action.long_press(elem, x, y, duration).perform()

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        """
        appium API
        Swipe from one point to another point, for an optional duration.
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
