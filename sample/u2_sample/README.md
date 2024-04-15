## 使用文档

* 安装依赖

```shell
pip install uiautomator2
```

### uiautomator2中使用poium

poium 本质上是一种模式，或者叫`语法糖`，所以，他不局限于selenium/appium，很高兴告诉你poium同样支持 playwright。

```python
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

```

* `Locator` 是 playwright 定位元素发方法，这里于原方法保持一致。
* `Locator` 支持的定位，参考：https://playwright.dev/python/docs/selectors
* 基于元素定位可以实现哪些操作，参考：https://playwright.dev/python/docs/api/class-locator

