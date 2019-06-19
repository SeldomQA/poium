from poium import Page, PageSelect, PageElement
from time import sleep


class SelectPage(Page):
    elm = PageElement(xpath="//select")


def test_select(browser):
    """
    测试选择框的操作
    :param browser:
    :return:
    """
    page = SelectPage(browser)

    page.get("http://www.w3school.com.cn/tiy/t.asp?f=html_select")
    page.switch_to_frame("i")
    PageSelect(page.elm, value="saab")
    sleep(2)
    PageSelect(page.elm, index=2)
    sleep(2)
    PageSelect(page.elm, text="Audi")
    sleep(2)

