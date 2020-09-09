from poium.common import logging


class CSSElement(object):
    """
    Only CSS selectors are supported.
    Please see help: http://www.w3school.com.cn/cssref/css_selectors.asp
    >> from page_objects import Page, CSSElements
    >> class MyPage(Page):
            input = CSSElements('.s_ipt')
            button = CSSElements('#su')
    """

    driver = None

    def __init__(self, css, index=None, describe=None):
        self.css = css
        if index is None:
            self.index = "0"
        else:
            self.index = str(index)
        self.desc = describe

    def __get__(self, instance, owner):
        if instance is None:
            return None
        global driver
        driver = instance.driver
        return self

    def clear(self):
        """
        JavaScript API, Only support css positioning
        Clears the text if it's a text entry element, Only support css positioning
        """
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.style.border="2px solid red";
                    elm.value = "";""".format(css=self.css, index=self.index)
        driver.execute_script(js)

    def set_text(self, value):
        """
        JavaScript API, Only support css positioning
        Simulates typing into the element.
        :param value: input text
        """
        logging.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.style.border="2px solid red";
                    elm.value = "{value}";""".format(css=self.css, index=self.index, value=value)
        driver.execute_script(js)

    def click(self):
        """
        JavaScript API, Only support css positioning
        Click element.
        """
        logging.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                   elm.style.border="2px solid red";
                   elm.click();""".format(css=self.css, index=self.index)
        driver.execute_script(js)

    def click_display(self):
        """
        JavaScript API, Only support css positioning
        Click on the displayed element, otherwise skip it.
        """
        logging.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = 'var elm = document.querySelector("' + self.css + '");' \
             ' if(elm != null){elm.style.border="2px solid red";elm.click();}'
        driver.execute_script(js)

    def display(self):
        """
        JavaScript API, Only support css positioning
        Display hidden elements
        """
        logging.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.style.display = "block";""".format(css=self.css, index=self.index)
        driver.execute_script(js)

    def remove_attribute(self, attribute):
        """
        JavaScript API, Only support css positioning
        Remove element attribute, Only support css positioning
        :param attribute:
        """
        logging.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.removeAttribute("{attr}");""".format(css=self.css, index=self.index, attr=attribute)
        driver.execute_script(js)

    def set_attribute(self, attribute, value):
        """
        JavaScript API, Only support css positioning
        Setting element attribute, Only support css positioning
        :param attribute:
        :param value:
        """
        logging.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.setAttribute("{attr}", "{value}");
                    """.format(css=self.css, index=self.index, attr=attribute, value=value)
        driver.execute_script(js)

    def clear_style(self):
        """
        JavaScript API, Only support css positioning
        Clear element styles.
        """
        logging.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                    elm.style="";""".format(css=self.css, index=self.index)
        driver.execute_script(js)

    def clear_class(self):
        """
        JavaScript API, Only support css positioning
        Clear element class
        """
        logging.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{index}];
                     elm.removeAttribute("class");""".format(css=self.css, index=self.index)
        driver.execute_script(js)

    def inner_text(self, text):
        """
        JavaScript API, Only support css positioning
        The innerText property sets the text content of the specified element, Only support css positioning
        :param text: Inserted text
        """
        logging.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{i}];
                     elm.innerText="{text}";""".format(css=self.css, i=self.index, text=text)
        driver.execute_script(js)

    def remove_child(self, child=0):
        """
        JavaScript API, Only support css positioning
        Remove a node from the child node list
        :param child: child of the child node
        """
        logging.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{i}];
                    elm.removeChild(elm.childNodes[{child}]);""".format(css=self.css, i=self.index, child=str(child))
        driver.execute_script(js)

    def click_parent(self):
        """
        JavaScript API, Only support css positioning
        Click the parent element of the element
        """
        logging.info(
            "Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelectorAll("{css}")[{i}];
                    elm.parentElement.click();""".format(css=self.css, i=self.index)
        driver.execute_script(js)
