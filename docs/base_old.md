# 旧的文档（< 0.6.0 版本）

# Page、PageElement 和 PageElements

首先，欢迎使用poium库，poium基于Selenium/appium实现Page Objects设计模式的测试库。对Selenium/appium的部分API进行封装，努力简化API的使用。

你可以将poium与任何Python单元测试框架(unittest、pytest)结合使用.


#### 1、简单的例子。
创建一个简单的LoginPage，并使用LoginPage完成登录。这里会用到```Page```和 ```PageElement```

```python
from poium import Page, PageElement
from selenium import webdriver

class LoginPage(Page):
    username = PageElement(id_='username')
    password = PageElement(id_='password')
    login_button = PageElement(css='input[type="submit"]')

driver = webdriver.Chrome()
page = LoginPage(driver)
page.get("https://login.xxx.com")
page.username.send_keys("username")
page.username.send_keys("password")
page.login_button.click()

```
#### 2、支持的定位方式
poium同样支持8种定位方式。

```python
from poium import Page, PageElement

class LoginPage(Page):
    elem_id = PageElement(id_='id')
    elem_name = PageElement(name='name')
    elem_class = PageElement(class_name='class')
    elem_tag = PageElement(tag='input')
    elem_link_text = PageElement(link_text='this_is_link')
    elem_partial_link_text = PageElement(partial_link_text='is_link')
    elem_xpath = PageElement(xpath='//*[@id="kk"]')
    elem_css = PageElement(css='#id')
```      

#### 3、设置元素超时时间
通过```timeout```参数设置超时时间，默认为10s。

```python
from poium import Page, PageElement

class BaiduPage(Page):
    search_input = PageElement(id_='kw', timeout=5)
    search_button = PageElement(id_='su', timeout=30)
```

#### 4、设置元素描述。
```describe``` 参数并无实际意义，当你页面元素很多时，用它来增加可读性。

```python
from poium import Page, PageElement

class LoginPage(Page):
    """
    登录page类
    """
    username = PageElement(css='#loginAccount', describe="用户名")
    password = PageElement(css='#loginPwd', describe="密码")
    login_button = PageElement(css='#login_btn', describe="登录按钮")
    user_info = PageElement(css="a.nav_user_name > span", describe="用户信息")

```

#### 5、增加log开关
`log` 有时找不到元素或元素定位的很慢，打开log开关，可以看到更多信息。

```python
from poium import Page, PageElement


class BaiduIndexPage(Page):
    search_input = PageElement(name='wdss', describe="搜索输入框", log=True)
    search_button = PageElement(id_='su', describe="搜索按钮", log=True)

```
执行日志：
```
2019-11-21 12:20:03,851 - INFO - 搜索输入框, 1 times search, ('name', 'wdss') 
2019-11-21 12:20:08,883 - INFO - 搜索输入框, 2 times search, ('name', 'wdss') 
2019-11-21 12:20:13,907 - INFO - 搜索输入框, 3 times search, ('name', 'wdss') 
...
```

#### 6、定义一组元素
需要定位一组元素，可以使用 ```PageElements```。

```python
from poium import Page, PageElement, PageElements

class BaiduPage(Page):
    search_key = PageElement(id_='kw')
    search_button = PageElement(id_='su')
    # 定位一组元素
    search_result = PageElements(xpath="//div/h3/a")

```

更多API，请查看右侧 ```Pages``` 列表。


## PageSelect类

Selenium所提供的下拉框操作并不太好用，为此poium提供了PageSelect类。

例如有以下选择框。

```html
<select>
  <option value="volvo">Volvo</option>
  <option value="saab">Saab</option>
  <option value="opel">Opel</option>
  <option value="audi">Audi</option>
</select>
```

使用方式如下：
```python
from poium import Page, PageSelect,, PageElement
from selenium import webdriver

class SelectPage(Page):
    select = PageElement(xpath="//select")

def test_select():
    """测试选择框的操作"""
    dr = webdriver.Chrome()
    page = SelectPage(dr)
    page.get("http://www.xxxx.com")

    PageSelect(page.select, value="saab")
    PageSelect(page.select, index=2)
    PageSelect(page.select, text="Audi")
    
```

```PageSelect```类第一个参数为```select```标签的对象，后面可以选择不同的方式定义选项。

* value 对应 ```value="volvo"```

* index 对应选项的索引，第1个选项，第2个选项...

* text 对应选项的名称。




