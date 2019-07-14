from poium import Page, CSSElement
from time import sleep


class BaiduPage(Page):
    search_input = CSSElement("#kw", describe="百度搜索框")
    search_button = CSSElement("#su", describe="百度按钮")
    icp = CSSElement("#cp", describe="备案信息")
    search_key = CSSElement(".res-gap-right16", describe="")


def test_clear_input_click(browser):
    """
    清除\输入\点击
    :param browser: 浏览器驱动
    :return:
    """
    page = BaiduPage(browser)
    page.get("https://www.baidu.com")
    page.clear(page.search_input)
    page.set_text(page.search_input, "poium")
    page.click(page.search_button)
    sleep(2)
    page.click_display(page.search_key)
    sleep(2)
    assert page.get_title == "poium_百度搜索"


def test_get_info(browser):
    """
    获取页面标题,URL,文本
    :param browser: 浏览器驱动
    :return:
    """
    page = BaiduPage(browser)
    page.get("https://www.baidu.com")
    sleep(2)
    title = page.get_title
    url = page.get_url
    text = page.get_text(page.icp)
    assert "百度一下，你就知道" == title
    assert "www.baidu.com" in url
    assert "京ICP证030173号" in text


def test_get_attribute(browser):
    """
    元素属性修改/获取/删除
    :param browser: 浏览器驱动
    :return:
    """
    page = BaiduPage(browser)
    page.get("https://www.baidu.com")
    page.set_attribute(page.search_input, "type", "password")
    value = page.get_attribute(page.search_input, "type")
    assert value == "password"

    page.remove_attribute(page.search_input, "name")
    value2 = page.get_attribute(page.search_input, "name")
    assert value2 is None




