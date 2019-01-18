from time import sleep
from page_objects import PageObject
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


class Page(PageObject):
    """
    selenium/appium extend API
    """

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

    def display(self, css_selector):
        """
        Display hidden elements, Only support css positioning
        """
        js = 'document.querySelector("{css}").style.display = "block";'.format(css=css_selector)
        self.run_script(js)

    def remove_attribute(self, css_selector, attribute):
        """
        Remove element attribute, Only support css positioning
        """
        js = 'document.querySelector("{css}").removeAttribute("{attr}");'.format(css=css_selector,
                                                                                 attr=attribute)
        self.run_script(js)

    def get_attribute(self, css_selector, attribute):
        """
        Get element attribute, Only support css positioning
        :return:
        """
        js = 'return document.querySelector("{css}").getAttribute("{attr}");'.format(
            css=css_selector, attr=attribute)
        return self.driver.execute_script(js)

    def set_attribute(self, css_selector, attribute, type_):
        """
        Setting element attribute, Only support css positioning
        """
        js = 'document.querySelector("{css}").setAttribute("{attr}", "{type}");'.format(css=css_selector,
                                                                                        attr=attribute,
                                                                                        type=type_)
        self.run_script(js)

    def click(self, css_selector):
        """
        Click element, Only support css positioning
        """
        js = 'document.querySelector("{css}").click();'.format(css=css_selector)
        self.run_script(js)

    def input(self, css_selector, value):
        """
        Simulates typing into the element. Only support css positioning
        """
        js = 'document.querySelector("{css}").value = "{value}";'.format(css=css_selector, value=value)
        self.run_script(js)

    def js_clear(self, css_selector):
        """
        Clears the text if it's a text entry element, Only support css positioning
        """
        js = 'document.querySelector("{css}").value = "";'.format(css=css_selector)
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
