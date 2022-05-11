from poium.common import logging
from poium.common.exceptions import CSSFindElementError
from selenium.common.exceptions import JavascriptException


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

    def __init__(self, css: str, index: int = 0, describe: str = ""):
        self.css = css
        self.index = str(index)
        self.desc = describe

    def __get__(self, instance, owner):
        if instance is None:
            return None
        global driver
        driver = instance.driver
        return self

    def _execute_javascript(self, js):
        """
        Run the javascript script
        """
        try:
            return driver.execute_script(js)
        except JavascriptException:
            raise CSSFindElementError("Element discovery failure. ", js)

    def clear(self) -> None:
        """
        JavaScript API
        Clears the text if it's a text entry element, Only support css positioning
        """
        logging.info(f"Clear input field. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.style.border="2px solid red";
                    elm.value = "";"""
        self._execute_javascript(js)

    def get_text(self, i: int = None) -> str:
        """
        JavaScript API
        Get element text content.
        :param i: index
        """
        if i is None:
            i = self.index
        else:
            i = str(i)
        logging.info(f"get text. {self.desc}")
        js = f"""return document.querySelectorAll("{self.css}")[{i}].textContent;"""
        return self._execute_javascript(js)

    def set_text(self, value: str) -> None:
        """
        JavaScript API
        Simulates typing into the element.
        :param value: input text
        """
        logging.info(f"set text. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.style.border="2px solid red";
                    elm.value = "{value}";"""
        self._execute_javascript(js)

    def click(self) -> None:
        """
        JavaScript API
        Click element.
        """
        logging.info(f"click element. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                   elm.style.border="2px solid red";
                   elm.click();"""
        self._execute_javascript(js)

    def click_display(self) -> None:
        """
        JavaScript API
        Click on the displayed element, otherwise skip it.
        """
        logging.info(f"Click on the displayed element. {self.desc}")
        js = 'var elm = document.querySelector("' + self.css + '");' \
             ' if(elm != null){elm.style.border="2px solid red";elm.click();}'
        self._execute_javascript(js)

    def display(self) -> None:
        """
        JavaScript API
        Display hidden elements
        """
        logging.info(f"display hidden element. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.style.display = "block";"""
        self._execute_javascript(js)

    def remove_attribute(self, attribute) -> None:
        """
        JavaScript API
        Remove element attribute
        :param attribute:
        """
        logging.info(f"remove element attribute. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.removeAttribute("{attribute}");"""
        self._execute_javascript(js)

    def set_attribute(self, attribute, value) -> None:
        """
        JavaScript API
        Setting element attribute
        :param attribute:
        :param value:
        """
        logging.info(f"setting element attribute. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.setAttribute("{attribute}", "{value}");
                    """
        self._execute_javascript(js)

    def clear_style(self) -> None:
        """
        JavaScript API
        Clear element styles.
        """
        logging.info(f"clear element styles. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.style="";"""
        self._execute_javascript(js)

    def clear_class(self) -> None:
        """
        JavaScript API
        Clear element class
        """
        logging.info(f"clear element class. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                     elm.removeAttribute("class");"""
        self._execute_javascript(js)

    def inner_text(self, text) -> None:
        """
        JavaScript API
        The innerText property sets the text content of the specified element, Only support css positioning
        :param text: Inserted text
        """
        logging.info(f"inner text. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                     elm.innerText="{text}";"""
        self._execute_javascript(js)

    def remove_child(self, child: int = 0) -> None:
        """
        JavaScript API
        Remove a node from the child node list
        :param child: child of the child node
        """
        logging.info(f"Remove a node from the child node list. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.removeChild(elm.childNodes[{child}]);"""
        self._execute_javascript(js)

    def click_parent(self) -> None:
        """
        JavaScript API
        Click the parent element of the element
        """
        logging.info(f"click the parent element of the element. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.parentElement.click();"""
        self._execute_javascript(js)

    def scroll(self, top=0, left=0) -> None:
        """
        JavaScript API
        Scroll the div element on the page
        """
        logging.info(f"scroll the div element on the page. {self.desc}")
        if top != 0:
            js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.scrollTop={top};"""
            self._execute_javascript(js)
        if left != 0:
            js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.scrollLeft={left};"""
            self._execute_javascript(js)

    def move_to(self) -> None:
        """
        JavaScript API
        Move the mouse over the element
        """
        logging.info(f"Move the mouse over the element. {self.desc}")
        js = f"""var elm = document.querySelectorAll("{self.css}")[{self.index}];
                    elm.dispatchEvent(new Event("mouseover"));"""
        self._execute_javascript(js)

    @property
    def value(self) -> str:
        """
        JavaScript API
        Gets the value of the element.
        """
        logging.info(f"get element value. {self.desc}")
        js = f"""return document.querySelectorAll("{self.css}")[{self.index}].value;"""
        return self._execute_javascript(js)
