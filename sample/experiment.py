from selenium import webdriver


# 封装
class Page(object):

    def __init__(self, driver):
        self.driver = driver


class CSSElement(object):

    driver = None

    def __init__(self, css):
        self.css = css

    def __get__(self, instance, owner):
        if instance is None:
            return None
        global driver
        driver = instance.driver
        return self

    def set_text(self, value):
        global driver
        driver.execute_script("""var elm = document.querySelector("{css}");
                    elm.style.border="2px solid red";
                    elm.value = "{value}";""".format(css=self.css, value=value))

    def click(self):
        global driver
        driver.execute_script("""var elm = document.querySelector("{css}");
                   elm.style.border="2px solid red";
                   elm.click();""".format(css=self.css))


# test
class baiduPage(Page):
    search_input = CSSElement("#kw")
    search_button = CSSElement("#kw")


dr = webdriver.Chrome()
dr.get("http://www.baidu.com")
page = baiduPage(dr)
page.search_input.set_text("poium")
page.search_button.click()

dr.close()





