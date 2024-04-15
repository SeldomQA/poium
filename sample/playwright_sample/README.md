## 使用文档

* 安装依赖

```shell
pip install pytest-playwright
```

* 安装浏览器

```shell
playwright install chromium
```

* 运行sample

```shell
pytest playwright_sample.py
```

### playwright中使用poium

poium 本质上是一种模式，或者叫`语法糖`，所以，他不局限于selenium/appium，很高兴告诉你poium同样支持 playwright。

```python
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
    bp.search_input.fill("playwright")
    bp.search_icon.highlight()
    bp.search_icon.screenshot(path="./image/search_icon.png")
    bp.search_icon.click()

    # 断言URL
    expect(page).to_have_title(re.compile("playwright"))
```

* `Locator` 是 playwright 定位元素发方法，这里于原方法保持一致。
* `Locator` 支持的定位，参考：https://playwright.dev/python/docs/selectors
* 基于元素定位可以实现哪些操作，参考：https://playwright.dev/python/docs/api/class-locator

