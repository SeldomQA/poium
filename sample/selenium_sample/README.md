# selenium and appium 使用文档

## Page 和 Element

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

## Element类元素操作方法

当我们定位到一个元素之后，`Elements` 类除了提供`click`点击和`send_keys`输入，还可以丰富的操作。

* selenium 常规操作

```python
from poium import Page, Element


class XxPage(Page):
    elem = Element("id=xx")


page = XxPage(driver)

""""element is existed """
page.elem.is_exist()

"""Clears the text if it's a text entry element."""
page.elem.clear()

"""
Simulates typing into the element.
If clear_before is True, it will clear the content before typing.
"""
page.elem.send_keys(value, clear_before=False)

"""Clicks the element."""
page.elem.click()

"""Submits a form."""
page.elem.submit()

"""This element's ``tagName`` property."""
tag = page.elem.tag_name

"""Clears the text if it's a text entry element."""
text = page.elem.text

"""The size of the element."""
size = page.elem.size

"""
Gets the given property of the element.
"""
page.elem.get_property(name)

"""Gets the given attribute or property of the element."""
page.elem.get_attribute(name)

"""Whether the element is visible to a user."""
page.elem.is_displayed()

"""
Returns whether the element is selected.
Can be used to check if a checkbox or radio button is selected.
"""
page.elem.is_selected()

"""Returns whether the element is enabled."""
page.elem.is_enabled()

"""
selenium API
Switches focus to the specified frame
"""
page.elem.switch_to_frame()

"""
selenium API
Moving the mouse to the middle of an element
"""
page.elem.move_to_element()

"""
selenium API
Holds down the left mouse button on an element.
"""
page.elem.click_and_hold()

"""
selenium API
Holds down the left mouse button on an element.
"""
page.elem.double_click()

"""
selenium API
Performs a context-click (right click) on an element.
"""
page.elem.context_click()

"""
selenium API
Holds down the left mouse button on the source element,
    then moves to the target offset and releases the mouse button.
:param x: X offset to move to.
:param y: Y offset to move to.
"""
page.elem.drag_and_drop_by_offset(x, y)

"""
selenium API
Refreshes the current page, retrieve elements.
"""
page.elem.refresh_element(timeout=10)
```

* Select 下拉框操作

```python

"""
selenium API
Select all options that have a value matching the argument. That is, when given "foo" this
    would select an option like:

    <option value="foo">Bar</option>

    :Args:
    - value - The value to match against

    throws NoSuchElementException If there is no option with specisied value in SELECT
"""
page.elem.select_by_value(value)

"""
selenium API
Select the option at the given index. This is done by examing the "index" attribute of an
    element, and not merely by counting.

    :Args:
    - index - The option at this index will be selected

    throws NoSuchElementException If there is no option with specisied index in SELECT
"""
page.elem.select_by_index(index)

"""
selenium API
Select all options that display text matching the argument. That is, when given "Bar" this
    would select an option like:

    <option value="foo">Bar</option>

    :Args:
    - text - The visible text to match against

    throws NoSuchElementException If there is no option with specisied text in SELECT
"""
page.elem.select_by_visible_text(text)
```

* appium 扩展操作

```python

"""
appium API
Sends text to the element.
"""
page.elem.set_text(keys)

"""
appium API
Gets the location of an element relative to the view.
Returns:
    dict: The location of an element relative to the view
"""
page.elem.location_in_view

"""
appium API
Set the value on this element in the application
"""
page.elem.set_value(value)
```

* 模拟键盘操作

```python
page.elem.input(text="")

page.elem.enter()

page.elem.select_all()

page.elem.cut()

page.elem.copy()

page.elem.paste()

page.elem.backspace()

page.elem.delete()

page.elem.tab()

page.elem.space()
```

## CSSElement类

有时我们需要借助JavaScript实现一些特殊的操作。poium提供了`CSSElement`类，已经帮你封装了这些操作。

```python
from poium import Page, CSSElement


class BaiduIndexPage(Page):
    elem = CSSElement('#kw')
    elem2 = CSSElement('#su')
```

注：`CSSElement`类不需要指定定位方式，仅支持`CSS`定位。

### CSSElement类提供的操作

```python


"""
Clears the text if it's a text entry element, Only support css positioning
"""
page.elem.clear()

"""
Simulates typing into the element.
:param value: input text
"""
page.elem.set_text(value)

"""
Click element.
"""
page.elem.click()

"""
Click on the displayed element, otherwise skip it.
"""
page.elem.click_display()

"""
Display hidden elements
"""
page.elem.display()

"""
Remove element attribute, Only support css positioning
:param attribute:
"""
page.elem.remove_attribute(attribute)

"""
Setting element attribute, Only support css positioning
:param attribute:
:param value:
"""
page.elem.set_attribute(attribute, value)

"""
Clear element styles.
"""
page.elem.clear_style()

"""
Clear element class
"""
page.elem.clear_class()

"""
The innerText property sets the text content of the specified element, Only support css positioning
:param text: Inserted text
"""
page.elem.inner_text(text)

"""
Remove a node from the child node list
:param child: child of the child node
"""
page.elem.remove_child(child=0)

"""
Click the parent element of the element
"""
page.elem.click_parent()

"""
scroll the div element on the page
"""
page.elem.scroll(top=0, left=0)

"""
Move the mouse over the element
"""
page.elem.move_to()
```