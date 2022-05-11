"""
uiautomator2 Library test demo
https://github.com/openatx/uiautomator2
"""
import uiautomator2 as u2
from poium.u2 import Page, Element, Setting

Setting.click_screenshots = False


class BBSPage(Page):
    search_input = Element(resourceId="com.meizu.flyme.flymebbs:id/ko", describe="搜索输入框")
    search_button = Element(resourceId="com.meizu.flyme.flymebbs:id/o1", describe="搜索按钮")
    search_result = Element(resourceId="com.meizu.flyme.flymebbs:id/a29", describe="搜索结果")



d = u2.connect()
d.app_start("com.meizu.flyme.flymebbs")
page = BBSPage(d)

page.search_input.click()
page.search_input.send_keys("flyme")
page.search_button.click()

result = page.search_result.get_text()
print(result)

d.app_stop("com.meizu.flyme.flymebbs")

