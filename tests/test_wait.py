from selenium import webdriver
from page_objects import PageWait, PageObject, PageElement


class BaiduPage(PageObject):
    elm = PageElement(id_="kw")
    elm2 = PageElement(id_="2222")


dr = webdriver.Chrome()

page = BaiduPage(dr)
page.get("https://www.baidu.com")

page.elm.send_keys("selenium")

PageWait(page.elm2)

