from page_objects import PageObject, PageElement, PageElements
from selenium import webdriver
from time import sleep


class BaiduPage(PageObject):
    setting = PageElement(css='div#u1 > a.pf')
    search_setting = PageElement(css=".setpref")


class JSPage(PageObject):
    frame = PageElement(id_="iframe")
    date = PageElement(id_="appDate")
    year_mouth_data = PageElements(css=".dwwo", describe="小时")


def test_move_to_element():
    """测试鼠标悬停"""
    dr = webdriver.Chrome()

    page = BaiduPage(dr)
    page.get("https://www.baidu.com")

    page.move_to_element(page.setting)
    page.search_setting.click()

    dr.quit()


def test_drag_and_drop_by_offset():
    """测试鼠标滑动日期控件"""
    dr = webdriver.Chrome()

    page = JSPage(dr)
    page.get("http://www.jq22.com/yanshi4976")

    page.switch_to_frame(page.frame)
    page.date.click()

    page.drag_and_drop_by_offset(page.year_mouth_data[0], 0, 3)
    sleep(2)
    page.drag_and_drop_by_offset(page.year_mouth_data[1], 0, 5)
    sleep(2)
    page.drag_and_drop_by_offset(page.year_mouth_data[2], 0, 10)
    sleep(2)

    dr.quit()
