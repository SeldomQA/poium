# Page 和 Element

通过`Page`类和 `Element`类实现Page层元素层的封装。

```python
# page层封装
from poium import Page, Element

class BaiduPage(Page):
    input = Element(id_="kw", describe="搜索输入框")
    button = Element(id_="su", describe="搜索按钮")
```
1. 创建页面类继承`Page`类。
2. 通过`Element`类定义元素。

## Element 类参数
Element类提供了几个参数。

```python
from poium import Page, Element

class BaiduPage(Page):
    input = Element(id_="kw", timeout=1, index=0, describe="搜索输入框")
    button = Element(id_="su", timeout=1, index=0, describe="搜索按钮")
```
* 第一个参数: 支持所有`Selenium/appium`的定位方式
```python
# selenium
css = "xx"
id_ = "xx"
name = "xx"
xpath = "xx"
link_text = "xx"
partial_link_text = "xx"
tag = "xx"
class_name = "xx"

# appium
ios_uiautomation = "xx"
ios_predicate = "xx"
ios_class_chain = "xx"
android_uiautomator = "xx"
android_viewtag = "xx"
android_data_matcher = "xx"
android_view_matcher = "xx"
windows_uiautomation = "xx"
accessibility_id = "xx"
image = "xx"
custom = "xx"
```

* timeout: 设置超时检查次数，默认为`5`。
* index: 设置元素索引，当你的定位方式默认匹配到多个元素时，默认返回第1个，即为`0`.
* describe: 设置元素描述，默认为`undefined`, 建议为每个元素增加描述。

## Elements类

有时候，我们poium返回的是一组元素对象，可以使用`Elements`类。

```python
from poium import Page, Element, Elements

class BaiduPage(Page):
    input = Element(id_="kw", describe="搜索输入框")
    button = Element(id_="su", describe="搜索按钮")
    results = Elements(xpath="//div/h3/a", describe="搜索结果") # 返回一组元素
```

