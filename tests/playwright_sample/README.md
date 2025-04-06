## 使用文档

* 安装依赖

```shell
> pip install pytest-playwright
```

* 安装浏览器

```shell
> playwright install chromium
```

* 运行sample

```shell
> pytest --browser=chromium --headed test_playwright.py
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

支持定位一组元素，通过下表筛选

```python
from poium.playwright import Page, Locator


class xxxPage(Page):
    more_elems = Locator('id=sb_form_q', describe="bing搜索框")


def test_playwright(page):
    # 获得元素
    page.goto("https://cn.bing.com")
    xp = xxxPage(page)

    # 统计元素数量
    count = xp.more_elems.count()
    print(count)
    # 通过下标指定第几个
    xp.more_elems.nth(1).fill("xxx")

    # 针对一组元素进行操作
    checkboxes = xp.more_elems.all()
    for i in range(3):
        checkboxes[i].check()

    #  结合 filter()进一步筛选
    active_tabs = xp.more_elems.filter(has_text="Active")

```

* `Locator` 是 playwright 定位元素发方法，这里与其保持一致。
* `Locator` 支持的定位，参考：https://playwright.dev/python/docs/selectors
* 基于元素定位可以实现哪些操作，参考：https://playwright.dev/python/docs/api/class-locator
