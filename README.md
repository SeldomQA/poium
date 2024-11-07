![](logo.png)

> Page Objects design pattern test library; support selenium、appium、playwright, etc

Page Objects 设计模式测试库；支持 selenium、appium、playwright 等。

## Features

* 极简的Page层的元素定义。
* 支持主流的 Web/App UI库。
* 对原生 API 无损。

__支持库：__

- [x] selenium ✔️
- [x] appium ✔️
- [x] playwright ✔️
- [x] uiautomator2 ✔️
- [x] facebook-wda ️ ✔️

## Installation

pip install:

```shell
> pip install poium
> pip install playwright [可选]
> pip install uiautomator2 [可选]
> pip install facebook-wda [可选]
```

If you want to keep up with the latest version, you can install with github repository url:

```shell
> pip install -U git+https://github.com/SeldomQA/poium.git@master
```

## Sample

### selenium/appium

`poium` 对 `selenium/appium` 提供了良好的支持。

👉 [详细文档](./tests/selenium_sample)

* selenium

```python
from selenium import webdriver
from poium import Page, Element, Elements


# page
class BaiduPage(Page):
    input = Element("#kw")
    button = Element("id=su")
    result = Elements("//div/h3/a", describe="搜索结果", timeout=2)


# selenium
driver = webdriver.Chrome()

page = BaiduPage(driver)
page.open("https://www.baidu.com")
page.input.send_keys("baidu")
page.button.click()

for r in page.result:
    print(r.text)

driver.close()
```

* appium

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options
from poium import Page, Element


# page
class CalculatorPage(Page):
    number_1 = Element("id=com.android.calculator2:id/digit_1")
    number_2 = Element("id=com.android.calculator2:id/digit_2")
    add = Element("id=com.android.calculator2:id/op_add")
    eq = Element("id=com.android.calculator2:id/eq")


# appium
capabilities = {
    "automationName": "UiAutomator2",
    "platformName": "Android",
    'appPackage': 'com.android.calculator2',
    'appActivity': '.Calculator'
}
options = UiAutomator2Options().load_capabilities(capabilities)
driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)

page = CalculatorPage(driver)
page.number_1.click()
page.add.click()
page.number_2.click()
page.eq.click()

driver.quit()
```

### playwright

`poium 1.2` 版本支持playwright库, 目前仅支持`sync`的用法.

👉 [详细文档](./tests/playwright_sample)

```python
import re
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from poium.playwright import Page, Locator


# page
class BingPage(Page):
    search_input = Locator('id=sb_form_q', describe="bing搜索框")
    search_icon = Locator('id=search_icon', describe="bing搜索按钮")


# playwright
with sync_playwright() as p:
    # 启动浏浏览器
    browser = p.chromium.launch(headless=False)
    # 创建新的页面
    page = browser.new_page()
    # 进入指定URL
    page.goto("https://cn.bing.com")

    # 获得元素
    search_page = BingPage(page)
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

### openatx

`openatx` 有国内是非常流行的移动App自动化工具，`poium`同样对它做了支持。

👉 [详细文档](./tests/u2_sample)

* uiautomator2

```python
import uiautomator2 as u2

from poium.u2 import Page, XpathElement


class BingPage(Page):
    search = XpathElement('//*[@resource-id="com.microsoft.bing:id/sa_hp_header_search_box"]')
    search_input = XpathElement('//*[@resource-id="com.microsoft.bing:id/sapphire_search_header_input"]')
    search_count = XpathElement('//*[@resource-id="count"]')


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

### seldom

seldom是一个全功能自动化测试框架。

👉 [详细文档](./tests/seldom_sample)

```python
import seldom
from poium import Page, Element


class BaiduPage(Page):
    """baidu page"""
    input = Element("id=kw", describe="搜索输入框")
    button = Element("id=su", describe="搜索按钮")


class BaiduTest(seldom.TestCase):
    """Baidu search test case"""

    def test_case(self):
        """A simple test"""
        page = BaiduPage()
        page.open("https://www.baidu.com")
        page.input.send_keys("seldom")
        page.button.click()
        self.assertTitle("seldom_百度搜索")


if __name__ == '__main__':
    seldom.main(browser='edge')
```

## 微信（WeChat）

> 欢迎添加微信，交流和反馈问题。

<div style="display: flex;justify-content: space-between;width: 100%">
    <p><img alt="微信" src="wechat.jpg" style="width: 200px;height: 100%" ></p>
</div>

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=SeldomQA/poium&type=Date)

## Project History

* [page-objects](https://github.com/eeaston/page-objects)

poium 参考 page-objects，他项目已经不再维护，原项目代码虽然只有100多行，但设计非常精妙。本项目在此基础上进行开发。

* [selenium-page-objects](https://pypi.org/project/selenium-page-objects/)

selenium-page-objects是poium的前身，为了简化项目名称，改名为poium。__po__ 取自 Page Object 首字母, __ium__
取自selenium/appium 共同后缀。
