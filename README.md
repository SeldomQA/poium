#### poium
---

<img src="./poium_logo.gif"  height="150">

基于 selenium/appium 的 Page Objects 设计模式测试库。

* 极大的简化了Page层的元素定义。
* 同时支持selenium和appium
* 通过JavaScript扩展了selenium API
* 对原生 API 无损

#### Installation
---

download install:

```shell
> python setup.py install
```

pip install:

```shell
> pip install poium
```

#### Sample

支持Selenium的例子。

```python
from poium import Page, PageElement
from selenium import webdriver


class BaiduIndexPage(Page):
    search_input = PageElement(name='wd')
    search_button = PageElement(id_='su')


driver = webdriver.Chrome()

page = BaiduIndexPage(driver)
page.get("https://www.baidu.com")

page.search_input = "poium"
page.search_button.click()

driver.quit()
```

还提供了一套JavaScript封装的API。

```python
from poium import Page, CSSElement
from selenium import webdriver


class BaiduIndexPage(Page):
    search_input = CSSElement('#kw')
    search_button = CSSElement('#su')


driver = webdriver.Chrome()

page = BaiduIndexPage(driver)
page.get("https://www.baidu.com")

page.set_text(page.search_input, "poium")
page.click(page.search_button)

driver.quit()
```

支持appium的例子。

```python
from poium import Page, PageElement
from appium import webdriver

class CalculatorPage(Page):
    number_1 = PageElement(id_="com.android.calculator2:id/digit_1")
    number_2 = PageElement(id_="com.android.calculator2:id/digit_2")
    add = PageElement(id_="com.android.calculator2:id/op_add")
    eq = PageElement(id_="com.android.calculator2:id/eq")

# APP定义运行环境
desired_caps = {
    'deviceName': 'Android Emulator',
    'automationName': 'appium',
    'platformName': 'Android',
    'platformVersion': '7.0',
    'appPackage': 'com.android.calculator2',
    'appActivity': '.Calculator',
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

page = CalculatorPage(driver)
page.number_1.click()
page.add.click()
page.number_2.click()
page.eq.click()

driver.quit()
```

使用poium将元素 __定位__ 与 __操作__ 分离，这将会非常有助于规模化自动化测试用例的编写与维护。

#### Documentation

请阅读 [wiki](https://github.com/defnngj/poium/wiki)

#### Project History

参考项目：https://github.com/eeaston/page-objects

参考项目已经不再维护，我阅读了原项目代码，虽然只有100多行，但设计非常精妙。本项目在此基础上进行开发。

原项目名：https://pypi.org/project/selenium-page-objects/

本项目的核心是 Page Objects设计模式, 于是取了 __PO__，同时支持selenium/appium，于是取了 __ium__，那么新的项目命名为：__poium__。
