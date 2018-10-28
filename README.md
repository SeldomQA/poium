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
pip install -i https://testpypi.python.org/pypi selenium-page-objects
```

#### Quick Example
-------------
```python
from page_objects import PageObject, PageElement

class LoginPage(PageObject):
    username = PageElement(id_='username')
    password = PageElement(id_='password')
    login = PageElement(css='input[type="submit"]')

```

#### Time Out Example
-------------
```python
from page_objects import PageObject, PageElement

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