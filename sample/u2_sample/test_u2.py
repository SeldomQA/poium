"""
uiautomator2 Library test demo
https://github.com/openatx/uiautomator2
"""
import uiautomator2 as u2

from poium.u2 import Page, XpathElement


class BingPage(Page):
    search = XpathElement('//*[@resource-id="com.microsoft.bing:id/sa_hp_header_search_box"]')
    search_input = XpathElement('//*[@resource-id="com.microsoft.bing:id/sapphire_search_header_input"]')
    search_count = XpathElement('//*[@resource-id="count"]')


def test_u2():
    d = u2.connect()
    d.app_start("com.microsoft.bing")
    page = BingPage(d)
    page.search.click()

    page.search_input.click()
    page.search_input.set_text("uiautomator2")
    page.press("enter")
    page.sleep(2)
    result = page.search_count.get_text()
    assert "个结果" in result

    d.app_stop("com.microsoft.bing")
