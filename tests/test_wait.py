from selenium import webdriver
from time import sleep
from page_objects import PageWait, PageObject, PageElement


class BaiduPage(PageObject):
    elm = PageElement(css=".loginFuncNormal", timeout=1)
    frame = PageElement(css="div#loginDiv > iframe", timeout=1)
    user = PageElement(name="email", timeout=1)


dr = webdriver.Chrome()

page = BaiduPage(dr)
page.get("https://www.126.com/")

page.elm.click()

# dr.switch_to.frame(page.frame)
# page.witch_to_frame(page.frame)
PageWait(page.user)
page.user.send_keys("fnngj")

sleep(10)
dr.quit()
