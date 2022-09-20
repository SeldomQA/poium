import re
from playwright.sync_api import expect
from poium.playwright import Page, Locator


class BingPage(Page):
    search_input = Locator('id=sb_form_q', describe="bing搜索框")
    search_icon = Locator('id=search_icon', describe="bing搜索按钮")


def test_playwright(page):
    # 获得元素
    page.goto("https://cn.bing.com")
    bing_page = BingPage(page)
    bing_page.search_input.highlight()
    bing_page.search_input.fill("playwright")
    bing_page.search_icon.highlight()
    bing_page.search_icon.screenshot(path="./image/search_icon.png")
    bing_page.search_icon.click()

    # 断言URL
    expect(page).to_have_title(re.compile("playwright"))
