# Page 和 Element

通过`Page`类和 `Element`类实现Page层元素层的定义。

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
    # **kwargs 定位
    input1 = Element(id_="kw", timeout=5, index=0, describe="搜索输入框")
    button1 = Element(css="#su", timeout=5, index=0, describe="搜索按钮")
    # selector 定位
    input2 = Element("id=kw", timeout=5, index=0, describe="搜索输入框")
    button2 = Element("#su", timeout=5, index=0, describe="搜索按钮")
```

* selector/ **kwgrer: 支持所有`Selenium/appium`的定位方式
* timeout: 设置超时检查次数，默认为`5`。
* index: 设置元素索引，当你的定位方式默认匹配到多个元素时，默认返回第1个，即为`0`.
* describe: 设置元素描述，建议为每个元素增加描述，方便维护。

> poium 1.3.0 引入新的 selector 定位，弱化了selenium/appium 的定位类型方式。

* `**kwargs` 和 `selector` 定位对比。

| 类型              | 定位                   | **kwargs                    | selector        |
|-----------------|----------------------|-----------------------------|-----------------|
| selenium/appium | id                   | id_="id"                    | "id=id"         |
| selenium        | mame                 | name="name"                 | "name=name"     |
| selenium/appium | class                | class_name="class"          | "class=class"   |
| selenium        | tag                  | tag="input"                 | "tag=input"     |
| selenium        | link_text            | link_text="文字链接"            | "text=文字链接"     |
| selenium        | partial_link_text    | partial_link_text="文字链"     | "text~=文字链"     |
| selenium/appium | xpath                | xpath="//*[@id='11']"       | "//*[@id='11']" |
| selenium        | css                  | cass="input#id"             | "input#id"      |
| appium          | ios_uiautomation     | ios_uiautomation = "xx"     | null            |
| appium          | ios_predicate        | ios_predicate = "xx"        | null            |
| appium          | ios_class_chain      | ios_class_chain = "xx"      | null            |
| appium          | android_uiautomator  | android_uiautomator = "xx"  | null            |
| appium          | android_viewtag      | android_viewtag = "xx"      | null            |
| appium          | android_data_matcher | android_data_matcher = "xx" | null            |
| appium          | android_view_matcher | android_view_matcher = "xx" | null            |
| appium          | windows_uiautomation | windows_uiautomation = "xx" | null            |
| appium          | accessibility_id     | accessibility_id = "xx"     | null            |
| appium          | image                | image = "xx"                | null            |
| appium          | custom               | custom = "xx"               | null            |


## Elements类

如果需要poium返回的是一组元素对象，可以使用`Elements`类。

```python
from poium import Page, Element, Elements

class BaiduPage(Page):
    input = Element(id_="kw", describe="搜索输入框")
    button = Element(id_="su", describe="搜索按钮")
    results = Elements(xpath="//div/h3/a", describe="搜索结果")  # 返回一组元素
```

