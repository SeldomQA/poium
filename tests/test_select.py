from page_objects import PageSelect, PageObject, PageElement
from selenium import webdriver
from time import sleep


class SelectPage(PageObject):
    elm = PageElement(xpath="//select")


dr = webdriver.Chrome()
page = SelectPage(dr)

page.get("http://www.w3school.com.cn/tiy/t.asp?f=html_select")
dr.switch_to.frame("i")
PageSelect(page.elm, value="saab")
sleep(2)
PageSelect(page.elm, index=2)
sleep(3)
PageSelect(page.elm, text="Audi")
sleep(5)

dr.quit()
