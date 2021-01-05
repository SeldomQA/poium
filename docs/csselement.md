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

page.elem.clear()
"""
JavaScript API, Only support css positioning
Clears the text if it's a text entry element, Only support css positioning
"""

page.elem.set_text(value)
"""
JavaScript API, Only support css positioning
Simulates typing into the element.
:param value: input text
"""

page.elem.click()
"""
JavaScript API, Only support css positioning
Click element.
"""


page.elem.click_display()
"""
JavaScript API, Only support css positioning
Click on the displayed element, otherwise skip it.
"""

page.elem.display()
"""
JavaScript API, Only support css positioning
Display hidden elements
"""

page.elem.remove_attribute(attribute)
"""
JavaScript API, Only support css positioning
Remove element attribute, Only support css positioning
:param attribute:
"""

page.elem.set_attribute(attribute, value)
"""
JavaScript API, Only support css positioning
Setting element attribute, Only support css positioning
:param attribute:
:param value:
"""

page.elem.clear_style()
"""
JavaScript API, Only support css positioning
Clear element styles.
"""
    
page.elem.clear_class()
"""
JavaScript API, Only support css positioning
Clear element class
"""

page.elem.inner_text(text)
"""
JavaScript API, Only support css positioning
The innerText property sets the text content of the specified element, Only support css positioning
:param text: Inserted text
"""

page.elem.remove_child(child=0)
"""
JavaScript API, Only support css positioning
Remove a node from the child node list
:param child: child of the child node
"""

page.elem.click_parent()
"""
JavaScript API, Only support css positioning
Click the parent element of the element
"""

page.elem.scroll(top=0, left=0)
"""
JavaScript API, Only support css positioning
scroll the div element on the page
"""

page.elem.move_to()
"""
JavaScript API, Only support css positioning
Move the mouse over the element
"""
```