from poium import Page, CSSElement
from time import sleep


class BaiduPage(Page):
    search_input = CSSElement("#kw", describe="百度搜索框")
    search_button = CSSElement("#su", describe="百度按钮")
    icp = CSSElement("#cp", describe="备案信息")
    search_key = CSSElement(".res-gap-right16", describe="")
    setting_dropdown_box = CSSElement("#s_user_name_menu", describe="设置下拉框")


def test_clear_input_click(browser):
    """
    清除\输入\点击
    :param browser: 浏览器驱动
    :return:
    """
    page = BaiduPage(browser)
    page.get("https://www.baidu.com")
    page.search_input.clear()
    page.search_input.set_text("poium")
    page.search_button.click()
    sleep(2)
    page.search_key.click_display()
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
    assert "百度一下，你就知道" == title
    assert "www.baidu.com" in url


def test_get_attribute(browser):
    """
    元素属性修改/获取/删除
    :param browser: 浏览器驱动
    :return:
    """
    page = BaiduPage(browser)
    page.get("https://www.baidu.com")
    page.search_button.remove_attribute("class")
    page.search_input.set_attribute("type", "password")
    page.search_input.set_text("abc123")
    sleep(5)



