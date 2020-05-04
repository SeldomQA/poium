from poium import Page, PageSelect
from poium import NewPageElement as PageElement
from time import sleep


class SelectPage(Page):
    frame = PageElement(id_="iframeResult", describe="表单")
    elm = PageElement(xpath="//select", describe="选择框")


def test_select(browser):
    """
    测试选择框的操作
    :param browser:
    :return:
    """
    page = SelectPage(browser)

    page.get("http://www.w3school.com.cn/tiy/t.asp?f=html_select")
    page.frame.switch_to_frame()
    PageSelect(page.elm, value="saab")
    sleep(2)
    PageSelect(page.elm, index=2)
    sleep(2)
    PageSelect(page.elm, text="Audi")
    sleep(2)

