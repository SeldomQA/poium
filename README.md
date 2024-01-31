
![](logo.png)

> Page Objects design pattern test library; support selenium、appium、playwright, etc

Page Objects 设计模式测试库；支持 selenium、appium、playwright 等。

## Features

* 极简的Page层的元素定义
* 对原生 API 无损
* 支持 logger 日志


__支持库：__

  - [x] [selenium](./docs/selenium_sample.md) ✔️
  - [x] [appium](./docs/appium_sample.md) ✔️
  - [x] [playwright](./docs/playwright_sample.md) ✔️
  - [ ] uiautomator2 ⌛
  - [ ] facebook-wda ⌛

## Installation

pip install:

```shell
> pip install poium
```

If you want to keep up with the latest version, you can install with github repository url:

```shell
> pip install -U git+https://github.com/SeldomQA/poium.git@master
```

## Demo

通过下面的例子，体会`Page Objects` 设计模式如此简单。

```python
from selenium import webdriver
from poium import Page, Element, Elements


class BaiduPage(Page):
    input = Element("#kw")
    button = Element("id=su")
    result = Elements("//div/h3/a", describe="搜索结果", timeout=2)


driver = webdriver.Chrome()

page = BaiduPage(driver)
page.open("https://www.baidu.com")
page.input.send_keys("baidu")
page.button.click()

for r in page.result:
    print(r.text)

driver.close()
```


更多例子，请点击[这里](/sample) 。

### Documentation

在开使用poium前，请快速阅读下面的文档。

* [Page和Element类](/docs/page_element.md)
* [Element类元素操作](docs/element_operation.md)
* [CSSElement类](/docs/csselement.md)

other：
* [seldom+poium](docs/seldom_sample.md)

## Project History

* [page-objects](https://github.com/eeaston/page-objects)

poium 参考page-objects，他项目已经不再维护，原项目代码虽然只有100多行，但设计非常精妙。本项目在此基础上进行开发。

* [selenium-page-objects](https://pypi.org/project/selenium-page-objects/)

selenium-page-objects是poium的前身，为了简化项目名称，改名为poium。__po__ 取自 Page Object 首字母, __ium__ 取自selenium/appium 共同后缀。
