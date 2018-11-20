### selenium_page_objects

基本 selenium 的Page objects设计模式。

#### Installation
------------

download install:
```shell
$ python setup.py install
```

pip install:
```
$ pip install -i https://test.pypi.org/simple/ selenium-page-objects
```

#### Quick Example
-------------
简单的例子：
```python
from page_objects import PageObject, PageElement

class LoginPage(PageObject):
    username = PageElement(id_='username')
    password = PageElement(id_='password')
    login = PageElement(css='input[type="submit"]')

```

#### Time Out Example
-------------
设置元素超时时间：
```python
from page_objects import PageObject, PageElement

class BaiduPage(PageObject):
    search_input = PageElement(id_='kw', timeout=3)
    search_button = PageElement(id_='su', timeout=10)
```

#### setting Describe Example
-------------
设置元素描述：
```python

class LoginPage(PageObject):
    """
    登录page类
    """
    username = PageElement(css='#loginAccount', describe="用户名")
    password = PageElement(css='#loginPwd', describe="密码")
    login_button = PageElement(css='#login_btn', describe="登录按钮")
    user_info = PageElement(css="a.nav_user_name > span", describe="用户信息")

```
describe 参数并无实际意义，当你页面元素很多时，用它来增加可读性。

#### Elements Example
-------------
定义一组元素（完整的例子）：
```python
from page_objects import PageObject, PageElement, PageElements
from selenium import webdriver
from time import sleep

class BaiduPage(PageObject):
    search_key = PageElement(id_='kw')
    search_button = PageElement(id_='su')
    # 定位一组元素
    search_result = PageElements(xpath="//div/h3/a")

driver = webdriver.Chrome()
page = BaiduPage(driver)
page.get("https://www.baidu.com")
page.search_key.send_keys("selenium")
page.search_button.click()
sleep(2)

for result in page.search_result:
    print(result.text)

```