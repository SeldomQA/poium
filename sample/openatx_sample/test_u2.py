"""
uiautomator2 Library test demo
https://github.com/openatx/uiautomator2
"""

from poium.u2 import Page, XpathElement, Element
from poium.u2.driver import Android


class BingPage(Page):
    news = XpathElement('//*[@text="News"]')
    tabs = Element(text="Tabs")


class BingSearchPage(Page):
    input = XpathElement('//*[@text="Search"]')


def test_bing_search():
    # app
    d = Android(package_name="com.microsoft.bing")
    d.connect()
    d.start_app()

    # page
    page = BingSearchPage(d.driver, d.package_name)
    page.input.click()
    page.input.set_text("poium")
    page.sleep(1)
    page.press(key="enter")
    page.sleep(2)

    # app
    d.close_app()


def test_bing_app():
    # app
    d = Android(package_name="com.microsoft.bing")
    d.connect()
    d.start_app()

    # page
    page = BingPage(d.driver, d.package_name)
    info = page.app_info()

    page.news.click()
    page.swipe_left(times=2)
    page.sleep(2)
    page.swipe_right()
    page.sleep(2)

    page.tabs.click()
    page.sleep(2)

    # app
    d.close_app()
