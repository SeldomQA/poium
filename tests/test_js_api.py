from page_objects import PageObject
from selenium import webdriver
from time import sleep


class BaiduPage(PageObject):
    search_input = "#kw"
    search_button = "#su"


dr = webdriver.Chrome()
page = BaiduPage(dr)

# 点击与输入
page.get("https://www.baidu.com")
page.js_input(page.search_input, "poium")
page.js_click(page.search_button)
sleep(2)

# 修改元素属性
page.get("https://www.baidu.com")
page.js_set_attribute(page.search_input, "type", "password")
page.js_input(page.search_input, "123456")
sleep(2)

# 获取元素属性与删除
page.get("https://www.baidu.com")
value = page.js_get_attribute(page.search_input, "name")
assert value == "wd"

page.js_remove_attribute(page.search_input, "name")
value2 = page.js_get_attribute(page.search_input, "name")
assert value2 is None

dr.quit()


