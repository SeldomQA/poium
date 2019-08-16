import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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

    def __init__(self, css, describe=None):
        self.css = css
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
        js = """var elm = document.querySelector("{css}");
                    elm.style.border="2px solid red";
                    elm.value = "";""".format(css=self.css)
        driver.execute_script(js)

    def set_text(self, value):
        """
        JavaScript API, Only support css positioning
        Simulates typing into the element.
        """
        logger.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelector("{css}");
                    elm.style.border="2px solid red";
                    elm.value = "{value}";""".format(css=self.css, value=value)
        driver.execute_script(js)

    def click(self):
        """
        JavaScript API, Only support css positioning
        Click element.
        """
        logger.info("Element of the current operation: {desc}".format(desc=self.desc))
        js = """var elm = document.querySelector("{css}");
                   elm.style.border="2px solid red";
                   elm.click();""".format(css=self.css)
        driver.execute_script(js)

    def click_display(self):
        """
        JavaScript API, Only support css positioning
        Click on the displayed element, otherwise skip it.
        """
        js = 'var elm = document.querySelector("' + self.css + '");' \
             ' if(elm != null){elm.style.border="2px solid red";elm.click();}'
        driver.execute_script(js)

    def display(self):
        """
        JavaScript API, Only support css positioning
        Display hidden elements
        """
        js = """var elm = document.querySelector("{css}");
                    elm.style.display = "block";""".format(css=self.css)
        driver.execute_script(js)

    def remove_attribute(self, attribute):
        """
        JavaScript API, Only support css positioning
        Remove element attribute, Only support css positioning
        """
        js = """var elm = document.querySelector("{css}");
                    elm.removeAttribute("{attr}");""".format(css=self.css, attr=attribute)
        driver.execute_script(js)

    def set_attribute(self, attribute, value):
        """
        JavaScript API, Only support css positioning
        Setting element attribute, Only support css positioning
        """
        js = """var elm = document.querySelector("{css}");
                    elm.setAttribute("{attr}", "{value}");
                    """.format(css=self.css, attr=attribute, value=value)
        driver.execute_script(js)

    def clear_style(self):
        """
        JavaScript API, Only support css positioning
        Clear element styles.
        """
        js = """var elm = document.querySelector("{css}");
                    elm.style.border="2px solid red";
                    elm.style="";""".format(css=self.css)
        driver.execute_script(js)

