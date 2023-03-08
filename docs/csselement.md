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