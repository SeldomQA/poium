### poium

基于 selenium/appium 的 Page Objects 设计模式测试库。

* 支持大部分selenium/appium API。
* 封装元素定位操作，以及少量原生API，同时并不影响原生API的使用。

#### Installation
------------

download install:

```shell
$ python setup.py install
```

pip install:
```
$ pip install poium
```

#### 例子对比：

原生selenium实现百度搜索设置。
```python
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select


dr = webdriver.Chrome()
dr.get("https://www.baidu.com")

sleep(3)

# 鼠标的操作
settings = dr.find_element_by_css_selector("div#u1 > a.pf")
ActionChains(dr).move_to_element(settings).perform()
sleep(2)
dr.find_element_by_class_name("setpref").click()
sleep(1)


# 单选框操作，简体中文
dr.find_element_by_id("SL_1").click()
sleep(3)

# 选择框操作
select_el = dr.find_element_by_id("nr")
Select(select_el).select_by_value("20")
sleep(2)

# 保存设置
dr.find_element_by_class_name("prefpanelgo").click()

# 警告框
aleart = dr.switch_to.alert
print(aleart.text)
aleart.accept()
sleep(3)

dr.quit()
```

使用poium实现百度搜索设置。

```python

# baidu_page.py
from page_objects import PageObject, PageElement

class BaiduIndexPage(PageObject):
    settings = PageElement(link_text="div#u1 > a.pf", describe="设置")
    search_setting = PageElement(css=".setpref", describe="搜索设置")
    language = PageElement(id_="SL_1", describe="简体中文")
    select_number = PageElement(id_="nr", describe="下拉选择框")
    save_setting = PageElement(css=".prefpanelgo", describe="保存设置")


# test_baidu.py
from selenium import webdriver
from page_objects import PageWait, PageSelect
from baidu_page import BaiduIndexPage


driver = webdriver.Chrome()

page = BaiduIndexPage(driver)
page.get("https://www.baidu.com")

# 鼠标悬停
page.move_to_element(page.settings)
page.search_setting.click()

# 选择语言
PageWait(page.language)
page.language.click()

# 操作下拉框
PageSelect(page.select_number, value="20")

# 保存设置
page.save_setting.click()

# 警告框
aleart_text = page.get_alert_text
print(aleart_text)
page.accept_alert()

driver.quit()
```
使用poium将元素 __定位__ 与 __操作__ 分离，这将会非常有助于规模化自动化测试用例的编写与维护。

#### 使用文档：

请阅读 [wiki](https://github.com/defnngj/poium/wiki)

#### 项目历史：

参考项目：https://github.com/eeaston/page-objects

参考项目已经不再维护，我阅读了原项目代码，虽然只有100多行，但设计非常精妙。本项目在此基础上进行开发。

原项目名：https://pypi.org/project/selenium-page-objects/

有一天，我向群里的同学推荐selenium-page-objects，有同学问是否支持appium，appium也是从selenium继承而来，我想为什么不能支持appium呢？
于是，加入了appium支持，但是 selenium-page-objects 已经不能表达对appium的支持，而且他似乎有点长了。

本项目的核心是 Page Objects的设计模式, 于是取了__PO__，同时支持selenium/appium，于是取了__ium__，那么新的项目命名为：__poium__。