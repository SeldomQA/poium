from poium import Page, CSSElement, Element
from time import sleep


class BaiduPage(Page):
    search_input = CSSElement("#kw", describe="百度搜索框")
    search_button = CSSElement("#su", describe="百度按钮")
    icp = CSSElement("#cp", describe="备案信息")
    search_key = CSSElement(".res-gap-right16", describe="")
    setting_dropdown_box = CSSElement("#s_user_name_menu", describe="设置下拉框")
    setting = CSSElement("#s-usersetting-top", describe="设置")


class SoPage(Page):
    setting = CSSElement("#hd_setting", describe="搜索设置")
    search = CSSElement("#search-button", describe="搜索按钮")


class RunoobPage(Page):
    iframe = Element(css="#iframeResult")
    div = CSSElement("html > body > div")


def test_move_to(browser):
    """
    鼠标悬停到元素上
    :param browser: 浏览器驱动
    :return:
    """
    page = BaiduPage(browser)
    page.get("https://www.baidu.com")
    page.set_window_size()
    page.setting.move_to()
    sleep(5)


def test_clear_input_click(browser):
    """
    清除/输入/点击
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
    sleep(2)
    page.search_button.remove_attribute("class")
    page.search_input.set_attribute("type", "password")
    page.search_input.set_text("abc123")
    sleep(5)


def test_display(browser):
    """
    显示隐藏的元素
    :param browser: 浏览器驱动
    :return:
    """
    page = SoPage(browser)
    page.get("https://www.so.com")
    page.setting.display()
    sleep(5)


def test_clear_class(browser):
    """
    清除元素的class属性
    :param browser: 浏览器驱动
    :return:
    """
    page = SoPage(browser)
    page.get("https://www.so.com")
    page.search.clear_class()
    sleep(5)


def test_scroll(browser):
    """
    测试操作页面内嵌滚动条
    :param browser: 浏览器驱动
    :return:
    """
    page = RunoobPage(browser)
    page.get("https://www.runoob.com/try/try.php?filename=tryjsref_onscroll")
    page.iframe.switch_to_frame()
    page.div.scroll(top=100)
    sleep(5)
