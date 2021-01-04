## 在 appium 中使用 poium

在appium中使用poium非常简单。

```python
from poium import Page, Element
from appium import webdriver


# page层定义
class CalculatorPage(Page):
    number_1 = Element(id_="com.android.calculator2:id/digit_1")
    number_2 = Element(id_="com.android.calculator2:id/digit_2")
    add = Element(id_="com.android.calculator2:id/op_add")
    eq = Element(id_="com.android.calculator2:id/eq")


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