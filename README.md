### selenium_page_objects

基本 selenium 的Page objects设计模式。

#### Installation
------------

```shell
$ git clone https://github.com/defnngj/selenium_page_objects
$ cd page-objects
$ python setup.py install
```

#### Quick Example
-------------
```python
from page_objects import PageObject, PageElement
from selenium import webdriver

class LoginPage(PageObject):
    username = PageElement(id_='username')
    password = PageElement(name='password')
    login = PageElement(css='input[type="submit"]')

driver = webdriver.Chrome()
driver.root_uri = "http://example.com"
page = LoginPage(driver)
page.get("/login")
page.username = 'secret'
page.password = 'squirrel'
assert page.username.text == 'secret'
page.login.click()
```

#### Time Out Example
-------------
```python
from page_objects import PageObject, PageElement
from selenium import webdriver

class BaiduPage(PageObject):
    search_input = PageElement(id_='kw', time_out=3)
    search_button = PageElement(id_='su', time_out=10)
```

#### Elements Example
-------------
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