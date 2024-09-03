import re
from playwright.sync_api import expect
from poium.playwright import Page, Locator


class BingPage(Page):
    search_input = Locator('id=sb_form_q', describe="bing搜索框")
    search_icon = Locator('id=search_icon', describe="bing搜索按钮")


def test_playwright(page):
    # 获得元素
    page.goto("https://cn.bing.com")
    bp = BingPage(page)
    bp.search_input.highlight()
    bp.search_input.clear()
    bp.search_input.fill("playwright")
    bp.search_icon.highlight()
    bp.search_icon.screenshot(path="./image/search_icon.png")
    bp.search_icon.click()

    # 断言URL
    expect(page).to_have_title(re.compile("playwright"))
