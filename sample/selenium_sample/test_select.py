from poium import Page
from poium import Element
from time import sleep


class SelectPage(Page):
    frame = Element(id_="iframeResult", describe="表单")
    select_elem = Element(xpath="//select", describe="选择框")


def test_select(browser):
    """
    测试选择框的操作
    :param browser:
    :return:
    """
    page = SelectPage(browser)

    page.open("https://www.runoob.com/try/try.php?filename=tryhtml_select")
    page.frame.switch_to_frame()
    page.select_elem.select_by_value("saab")
    sleep(2)
    page.select_elem.select_by_index(2)
    sleep(2)
    page.select_elem.select_by_visible_text("Audi")
    sleep(2)

