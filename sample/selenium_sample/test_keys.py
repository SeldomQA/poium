from poium import Page
from poium import Element


class BaiduIndexPage(Page):
    search_input = Element(name='wd', describe="搜索框")


def test_keys(browser):
    page = BaiduIndexPage(browser)
    page.get("https://www.baidu.com")

    # 输入 seldomm
    page.search_input.input("seldomm")

    # 删除多输入的一个m
    page.search_input.backspace()

    # 输入空格键+“教程”
    page.search_input.space()
    page.search_input.input("教程")

    # ctrl+a 全选输入框内容
    page.search_input.select_all()

    # ctrl+x 剪切输入框内容
    page.search_input.cut()

    # ctrl+v 粘贴内容到输入框
    page.search_input.paste()

    # 通过回车键来代替单击操作
    page.search_input.enter()
