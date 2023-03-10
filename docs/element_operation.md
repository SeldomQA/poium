# Element类元素操作方法

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