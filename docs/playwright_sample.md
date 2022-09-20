## 在 poium 中使用 playwright

poium 本质上是一种模式，或者叫`语法糖`，所以，他不局限于selenium/appium，很高兴告诉你poium同样支持 playwright。

```python
import re
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from poium.playwright import Page, Locator


class SearchPage(Page):
    search_input = Locator('id=sb_form_q', describe="搜索")
    search_icon = Locator('id=search_icon', describe="按钮")


with sync_playwright() as p:
    # 启动浏浏览器
    browser = p.chromium.launch(headless=False)
    # 创建新的页面
    page = browser.new_page()
    # 进入指定URL
    page.goto("https://cn.bing.com")

    # 获得元素
    search_page = SearchPage(page)
    search_page.search_input.highlight()
    search_page.search_input.fill("playwright")
    search_page.search_icon.highlight()
    search_page.search_icon.screenshot(path="./docs/abc.png")
    search_page.search_icon.click()

    # 断言URL
    expect(page).to_have_title(re.compile("playwright"))

    # 关闭浏览器
    browser.close()
```

* `Locator` 是 playwright 定位元素发方法，这里于原方法保持一致。
* `Locator` 支持的定位：https://playwright.dev/python/docs/selectors


