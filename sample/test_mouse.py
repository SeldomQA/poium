from poium import Page, PageElement, CSSElement, PageElements
from time import sleep


class BaiduPage(Page):
    setting = PageElement(css='div#u1 > a.pf')
    search_setting = PageElement(css=".setpref")
    search_setting_hint = PageElement(css="#sugConf th")


class DataTimePage(Page):
    frame = PageElement(id_="iframe")
    date = PageElement(id_="appDate")
    year_mouth_data = PageElements(css=".dwwo")


def test_move_to_element(browser):
    """
    测试鼠标悬停
    :param browser:
    :return:
    """
    page = BaiduPage(browser)
    page.get("https://www.baidu.com")
    page.click_and_hold(page.setting)
    page.search_setting.click()
    sleep(2)
    hint = page.search_setting_hint.text
    assert hint == "搜索框提示："


def test_drag_and_drop_by_offset(browser):
    """
    测试鼠标滑动日期控件
    :param browser:
    :return:
    """
    page = DataTimePage(browser)
    page.get("http://www.jq22.com/yanshi4976")

    page.switch_to_frame(page.frame)
    page.date.click()

    page.drag_and_drop_by_offset(page.year_mouth_data[0], 0, 3)
    sleep(2)
    page.drag_and_drop_by_offset(page.year_mouth_data[1], 0, 5)
    sleep(2)
    page.drag_and_drop_by_offset(page.year_mouth_data[2], 0, 10)
    sleep(2)
